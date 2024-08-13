from collections import deque

from pycryptosat import Solver

import display.affichage as af
import mealymachinemodel.mealymachine as mm
import mealymachineproduct.productalgorithms as pa


class Var:
    # This class is used to generate unique variable ids
    num = 1
    id: int
    def __init__(self):
        self.id = Var.num
        Var.num += 1

class Ltm:
    # This class represents a linear trace machine
    ltm : mm.MealyMachine

    def __init__(self, input_alphabet, output_alphabet):
        # This function initializes the linear trace machine with the given input and output alphabets
        # The linear trace machine has only one state q0 at the beginning
        self.ltm = mm.MealyMachine(input_alphabet, output_alphabet)
        self.ltm.set_name("ltm")
        self.ltm.add_state(mm.State("q0"))
        self.ltm.set_initial_state(0)

    def expand_ltm_from_trace(self, trace):
        # This function expands the linear trace machine with the given trace
        # The trace is a list of tuples where each tuple contains an input and an output
        # The function adds a new state for each input-output pair in the trace
        # and adds a transition from the last state in the ltm to the new state
        # with the input and output from the trace
        nstates = len(self.ltm.get_states())
        for i in range(len(trace)):
            self.ltm.add_state(mm.State(f"q{nstates+i}"))
            if i == 0 and nstates == 1:
                self.ltm.add_transition(0, trace[i][0], trace[i][1], 1)
            else:
                self.ltm.add_transition(nstates+i-1, trace[i][0], trace[i][1], nstates+i)

# Global variables

global_ltm = None
formula = Solver()
partitions = []
parts_added = 0
v_var_map = {}
e_var_map = {}

def init_global_ltm(input_alphabet, output_alphabet):
    # This function initializes the global linear trace machine with the given input and output alph
    global global_ltm
    global_ltm = Ltm(input_alphabet, output_alphabet)

def expand_global_ltm_from_trace(trace):
    # This function expands the global linear trace machine with the given trace
    if global_ltm is not None:
        global_ltm.expand_ltm_from_trace(trace)
        global_ltm.ltm.set_name("ltm")
        af.show_mealy_machine(global_ltm.ltm)
    else:
        print("Global LTM not initialized")

def get_global_ltm():
    # This function returns the global linear trace machine
    return global_ltm

def get_global_formula():
    # This function returns the global formula
    return formula

def get_global_v_var_map():
    # This function returns the global v_var_map
    return v_var_map

def get_global_e_var_map():
    # This function returns the global e_var_map
    return e_var_map

def get_parts_added():
    # This function returns the global parts_added
    return parts_added

def get_global_partitions():
    # This function returns the global partitions
    return partitions

def reset_global_ltm():
    # This function resets the global linear trace machine
    global global_ltm
    global_ltm = None

def reset_formula():
    # This function resets the global formula
    global formula
    formula = Solver()

def reset_v_var_map():
    # This function resets the global v_var_map
    global v_var_map
    v_var_map = {}

def reset_e_var_map():
    # This function resets the global e_var_map
    global e_var_map
    e_var_map = {}

def reset_partitions():
    # This function resets the global partitions
    global partitions
    partitions = []

def reset_parts_added():
    # This function resets the global parts_added
    global parts_added
    parts_added = 0

def reset_all():
    # This function resets all the global variables
    reset_global_ltm()
    reset_formula()
    reset_v_var_map()
    reset_e_var_map()
    reset_partitions()
    reset_parts_added()

def not_compatible_sates(state1, state2):
    # This function returns True if the given states are not compatible
    # Two states are not compatible if they have transitions with the same input and output
    # but different arrival states
    for tr in state1.get_transitions():
        for tr2 in state2.get_transitions():
            if tr.get_input() == tr2.get_input() and tr.get_output() != tr2.get_output():
                return True
    return False

def compatible_states(state1, state2):
    # This function checks if two states are compatible
    # Two states are compatible if they have a transition with the same input and output
    # because the linear trace machine has only one transition per state
    # if the input and output of one transition are the same in both states, then we checked all the transitions
    # therefore the states are compatible
    assert(len(state1.get_transitions()) == 1)
    assert(len(state2.get_transitions()) == 1)
    for tr in state1.get_transitions():
        for tr2 in state2.get_transitions():
            if tr.get_input() == tr2.get_input() and tr.get_output() == tr2.get_output():
                return True
    return False  

def get_arrival_state(state):
    # This function returns the arrival state of the given state assuming that the state has only one transition
    # This assumption is valid for the linear trace machine
    res_state = list()
    for tr in state.get_transitions():
       res_state.append(tr.get_tgt())
    return res_state 

def init_partition_formula(nstates):
    #print("init_partition_formula")
    # This function initializes the partition formula for the given number of partitions
    global formula
    global v_var_map
    global e_var_map
    v_clause = []
    state0 = global_ltm.ltm.get_state(0)
    for i in range(nstates):
        #print(f"adding v_var for {state0.get_name()} and {i}")
        var_id = Var()
        v_var_map[(state0, i)] = var_id
        v_clause.append(var_id.id)
    formula.add_clause(v_clause)
    for i in range(nstates):
        for j in range(i+1, nstates):
            n_v_clause = []
            n_v_clause.append(-v_var_map[(state0, i)].id)
            n_v_clause.append(-v_var_map[(state0, j)].id)
            formula.add_clause(n_v_clause)

def extend_partition_formula(trace, nstates):
    # This function extends the partition formula for the given trace and number of partitions 
    # using the former formula stored in the global formula variable 
    # and the former linear trace machine (ltm) stored in the global_ltm variable
    # The formula is extended with the new states and transitions from the trace
    # at initialization, the lstm has only one state q0 and the formula is empty
    global formula
    global v_var_map
    global e_var_map
    init_ltm_size = len(global_ltm.ltm.get_states())
    expand_global_ltm_from_trace(trace) #Expand the linear trace machine with the given trace
    final_ltm_size = len(global_ltm.ltm.get_states())
    #Extend partition formula for clauses 2 and 3 for the rest of the states
    # print(f"init_ltm_size: {init_ltm_size}")
    # print(f"final_ltm_size: {final_ltm_size}")
    for i in range(init_ltm_size, final_ltm_size):
        v_clause = []
        curr_state = global_ltm.ltm.get_state(i)
        for j in range(nstates):
            if not (curr_state, j) in v_var_map:
                #print(f"adding v_var for {curr_state.get_name()} and {j}")
                var_id = Var()
                v_var_map[(curr_state, j)] = var_id
            else:
                var_id = v_var_map[(curr_state, j)]
            v_clause.append(var_id.id)
        formula.add_clause(v_clause)
    for s in range(init_ltm_size, final_ltm_size):
        curr_state = global_ltm.ltm.get_state(s)
        for i in range(nstates):
            for j in range(i+1, nstates):
                n_v_clause = []
                n_v_clause.append(-v_var_map[(curr_state, i)].id)
                n_v_clause.append(-v_var_map[(curr_state, j)].id)
                formula.add_clause(n_v_clause)
    #Extend partition formula for clause 6 and 7
    for i in range(init_ltm_size-1, final_ltm_size-1):
        curr_state1 = global_ltm.ltm.get_state(i)
        for j in range(final_ltm_size-1):
            curr_state2 = global_ltm.ltm.get_state(j)
            #Clause 6
            if not_compatible_sates(curr_state1, curr_state2):
                #print(f"States {curr_state1.get_name()} and {curr_state2.get_name()} are not compatible")
                if not (curr_state1, curr_state2) in e_var_map:
                    #print(f"adding e_var for {curr_state1.get_name()} and {curr_state2.get_name()}")
                    e_var = Var()
                    e_var_map[(curr_state1, curr_state2)] = e_var
                else:
                    e_var = e_var_map[(curr_state1, curr_state2)]
                e_clause = [-e_var.id]
                formula.add_clause(e_clause)
            #Clause 7
            if compatible_states(curr_state1, curr_state2):
                #print(f"States {curr_state1.get_name()} and {curr_state2.get_name()} are compatible")
                if not (curr_state1, curr_state2) in e_var_map:
                    #print(f"adding e_var for {curr_state1.get_name()} and {curr_state2.get_name()}")
                    e_var = Var()
                    e_var_map[(curr_state1, curr_state2)] = e_var
                else:
                    e_var = e_var_map[(curr_state1, curr_state2)]
                arr_state1 = get_arrival_state(curr_state1)
                arr_state2 = get_arrival_state(curr_state2)
                if not (arr_state1[0], arr_state2[0]) in e_var_map:
                    #print(f"adding e_var for {arr_state1[0].get_name()} and {arr_state2[0].get_name()}")
                    e_var2 = Var()
                    e_var_map[(arr_state1[0], arr_state2[0])] = e_var2
                else:
                    e_var2 = e_var_map[(arr_state1[0], arr_state2[0])]
                e_clause = [-e_var.id, e_var2.id]
                formula.add_clause(e_clause)
    #Extend partition formula for clause 8 and 9
    for i in range(init_ltm_size, final_ltm_size):
        curr_state1 = global_ltm.ltm.get_state(i)
        for j in range(final_ltm_size):
            curr_state2 = global_ltm.ltm.get_state(j)
            for k in range(nstates):
                if not (curr_state1, curr_state2) in e_var_map:
                    #print(f"adding e_var for {curr_state1.get_name()} and {curr_state2.get_name()}")
                    e_var = Var()
                    e_var_map[(curr_state1, curr_state2)] = e_var
                else:
                    e_var = e_var_map[(curr_state1, curr_state2)]
                if not (curr_state1, k) in v_var_map:
                    #print(f"adding v_var for {curr_state1.get_name()} and {k}")
                    v_var = Var()
                    v_var_map[(curr_state1, k)] = v_var
                else:
                    v_var = v_var_map[(curr_state1, k)]
                if not (curr_state2, k) in v_var_map:
                    #print(f"adding v_var for {curr_state2.get_name()} and {k}")
                    v_var2 = Var()
                    v_var_map[(curr_state2, k)] = v_var2
                else:
                    v_var2 = v_var_map[(curr_state2, k)]
                e_clause1 = [-e_var.id, -v_var.id, v_var2.id] #Clause 8
                e_clause2 = [e_var.id, -v_var.id, -v_var2.id] #Clause 9
                formula.add_clause(e_clause1)
                formula.add_clause(e_clause2)
                # Final formula conjunction of clauses 2, 3, 6, 7, 8 and 9

def get_state_partition(state, nstates, partition):
    # This function returns the partition of the given state
    global v_var_map
    for i in range(nstates):
        var = v_var_map[(state, i)]
        if partition[var.id]:
            return i
    return -1

def infer_conjecture(trace, nstates):
    # This function infers the conjecture from the given trace and number of partitions as precised in the paper
    # The function returns the solution of the formula if it exists
    global partitions
    global parts_added
    global formula
    global v_var_map
    global e_var_map
    global global_ltm
    #print("infer_conjecture")
    ltm_size = len(global_ltm.ltm.get_states())
    for part in range(parts_added, len(partitions)):
        #print(f"part: {part}")
        clause = []
        for e in e_var_map:
            var = e_var_map[e]
            if partitions[part][var.id]:
                clause.append(-var.id)
        formula.add_clause(clause)
    parts_added = len(partitions)
    extend_partition_formula(trace, nstates)
    sat, solution = formula.solve()
    if sat:
        #print("Solution found")
        return solution
    else:
        #print("No solution found")
        return None

def get_states_in_same_partition(partition, nstates):
    # This function returns the states that are in the same partition
    # The states are grouped by partition
    # The function returns a dictionary where the key is the partition number and the value is a list of states in that partition
    global global_ltm
    global v_var_map
    states = global_ltm.ltm.get_states()
    res = {}
    for i in range(nstates):
        res[i] = []
        for state in states:
            if get_state_partition(state, nstates, partition) == i:
                res[i].append(state)
    return res
          
def get_partition_with_ltm_initial_state(nstates, partition):
    # This function returns the partition containing the initial state of the linear trace machine
    global global_ltm
    initial_state = global_ltm.ltm.get_initial_state()
    return get_state_partition(initial_state, nstates, partition)

def get_partition_machine(nstates, partition):
    # This function returns the partition machine for the given number of partitions and partition
    # The partition machine is a mealy machine with the same input and output alphabets as the global linear trace machine
    # The partition machine has a state for each partition and contains all the transitions of the global linear trace machine
    # The transitions are calculated based on the partition of the states in the global linear trace machine
    # if the ltm contains a transition from state1 to state2 with input i and output o and state1 is in partition p1 and state2 is in partition p2
    # then the partition machine contains a transition from p1 to p2 with input i and output o
    # The initial state of the partition machine is the partition containing the initial state of the global linear trace machine
    machine = mm.MealyMachine(global_ltm.ltm.get_input_alphabet(), global_ltm.ltm.get_output_alphabet())
    machine.set_name("partition_machine")
    initial_state = get_partition_with_ltm_initial_state(nstates, partition)
    machine.set_initial_state(initial_state)
    #print(f"Initial state of the partition machine: {initial_state}")
    for i in range(nstates):
        machine.add_state(mm.State(f"q{i}"))
    states_per_partition = get_states_in_same_partition(partition, nstates)
    for i in range(nstates):
        for state in states_per_partition[i]:
            for tr in state.get_transitions():
                input = tr.get_input()
                output = tr.get_output()
                tgt = tr.get_tgt()
                tgt_partition = get_state_partition(tgt, nstates, partition)
                #if not machine.transition_exist(i, input, output, tgt_partition):
                machine.add_transition(i, input, output, tgt_partition)
    return machine

def extract_input_sequence_from_trace(trace):
    # This function extracts the input sequence from the trace
    return [x[0] for x in trace]

def extract_output_sequence_from_trace(trace):
    # This function extracts the output sequence from the trace
    return [x[1] for x in trace]

def get_transitions_inputs(state):
    # This function returns the inputs of the transitions of the given state
    return [tr.get_input() for tr in state.get_transitions()]

def find_extra_transition(state1, state2):
    # This function finds the extra transitions between two states
    # The extra transitions are the transitions with an input that is not in the inputs of the transitions of the other state
    state2_inputs = get_transitions_inputs(state2)
    state1_transitions = state1.get_transitions()
    for tr in state1_transitions:
        if tr.get_input() not in state2_inputs:
            return tr
        
def check_acceptance(machine, trace):
    iseq = extract_input_sequence_from_trace(trace)
    out = machine.computeanouputsequence(iseq)
    oseq = extract_output_sequence_from_trace(trace)
    return out[0] == oseq

def shortest_distinguishing_trace(machine1, machine2, init_trace): 
    # This function returns the shortest distinguishing trace between two machines
    # The trace is a list of tuples where each tuple contains an input and an output
    # The function returns the trace that distinguishes the two machines
    # If the two machines are equivalent, the function returns an empty trace

    if not check_acceptance(machine1, init_trace) or not check_acceptance(machine2, init_trace):
        raise Exception("Trace not recognized by one of the machines")
    
    iseq = extract_input_sequence_from_trace(init_trace)
    arr_state1 = machine1.get_state_of_arrival(iseq) if iseq else machine1.get_initial_state()
    arr_state2 = machine2.get_state_of_arrival(iseq) if iseq else machine2.get_initial_state()
    seen_states = set()
    states_to_visit = deque([(arr_state1, arr_state2, [], 0)])

    # Breadth-first search
    # We explore all the possible traces that distinguish the two machines
    # We stop when we find a trace that distinguishes the two machines
    # We keep track of the maximum length of the trace to avoid exploring longer traces
    # The trace is the shortest one that distinguishes the two machines

    while states_to_visit:
        state1, state2, trace, curr_len = states_to_visit.popleft()
        seen_states.add((state1, state2))
        n_of_transitions_state1 = len(state1.get_transitions())
        n_of_transitions_state2 = len(state2.get_transitions())
        # print(f"state1: {state1.get_name()}")
        # print(f"state2: {state2.get_name()}")
        # print(f"trace: {trace}")

        # if curr_len + 1 > max_len: # We stop exploring if the current trace is longer than the maximum length
        #     assert(False)
        #     continue

        if not state1.get_transitions() and not state2.get_transitions(): # If both machines have no transitions, we stop exploring
            assert(False)
            continue

        if not state1.get_transitions(): # If machine 1 has no transitions, we raise an exception because machine 1 should be complete
            assert(False)
        
        if not state2.get_transitions(): # If machine 2 has no transitions, we add the input and output of the first transition of machine 1 to the trace
            #print("machine 2 has no transitions")
            tr = state1.get_transitions()[0]
            new_trace = trace + [(tr.get_input(), tr.get_output())]
            return new_trace

        if n_of_transitions_state1 > n_of_transitions_state2: # If machine 1 has more transitions than machine 2, we add a transition with an input that is not in machine 2 to the trace
            #print("machine 1 has more transitions than machine 2")
            tr = find_extra_transition(state1, state2)
            new_trace = trace + [(tr.get_input(), tr.get_output())]
            return new_trace

        # If there are transitions in both machines, we compare the transitions
        # If the inputs are the same, we create a new trace with the input and output of the transitions to avoid calculating this value twice
        # If the outputs are different, we found a distinguishing trace and we update the maximum length and the result trace
        # If the outputs are the same, we add the target states to the queue to explore them later
        # We add the new trace to the queue with the target states and the current length + 1
        #print("comparing transitions")
        for tr in state1.get_transitions():
            for tr2 in state2.get_transitions():
                if tr.get_input() == tr2.get_input():
                    new_trace = trace + [(tr.get_input(), tr.get_output())]
                    if tr.get_output() != tr2.get_output():
                        return new_trace
                    else: 
                        tgt1 = tr.get_tgt()
                        tgt2 = tr2.get_tgt()
                        if (tgt1, tgt2) not in seen_states:
                            states_to_visit.append((tgt1, tgt2, new_trace, curr_len + 1))
    return []

def print_partition(partition, nstates):
    global v_var_map
    global e_var_map
    for key in v_var_map:
        state = key[0].get_name()
        part = key[1]
        print(f"v_var({state}, {part}): {partition[v_var_map[key].id]}")
    for key in e_var_map:
        state1 = key[0].get_name()
        state2 = key[1].get_name()
        print(f"e_var({state1}, {state2}): {partition[e_var_map[key].id]}")

def checking_sequence(machine):
    # This function calculates the checking sequence for the given machine
    # The checking sequence is a sequence that distinguishes an n state machine given in input from every other n state machine
    # This function assumes that the machine given in input is complete, strongly connected and deterministic
    # We calculate the checking sequence as shown in the paper
    global partitions
    init_global_ltm(machine.get_input_alphabet(), machine.get_output_alphabet())
    trace = []
    nstates = len(machine.get_states())
    init_partition_formula(nstates)
    part = infer_conjecture(trace, nstates)
    i = 0
    while part is not None:
        print(f"checking sequence iteration: {i}")
        print(f"omega trace: {trace}")
        pm = get_partition_machine(nstates, part)
        af.show_mealy_machine(pm)
        tr = shortest_distinguishing_trace(machine, pm, trace)
        if tr == []:
            #print("trace is empty")
            partitions.append(part)
            part = infer_conjecture(tr, nstates)
        else:
            #print("trace is not empty")
            trace += tr
            part = infer_conjecture(tr, nstates)
        i += 1
    reset_all()
    return trace

def main():
    dummy_machine = mm.MealyMachine(["a", "b"], ["0", "1"])
    dummy_machine.add_state(mm.State("q0"))
    dummy_machine.add_state(mm.State("q1"))
    dummy_machine.add_state(mm.State("q2"))
    dummy_machine.set_initial_state(0)
    dummy_machine.add_transition(0, "a", "0", 1)
    # dummy_machine.add_transition(0, "b", "1", 2)
    # dummy_machine.add_transition(1, "b", "0", 0)
    dummy_machine.add_transition(1, "a", "1", 2)
    # dummy_machine.add_transition(2, "a", "0", 1)
    dummy_machine.add_transition(2, "b", "0", 0)    
    dummy_machine.set_name("dummy_machine")
    af.show_mealy_machine(dummy_machine)
    dummy_machine.complete_with_self_loops()
    dummy_machine.set_name("dummy_machine2")
    af.show_mealy_machine(dummy_machine)
    # check = checking_sequence(dummy_machine)
    # print(check)

main()