#https://graphviz.readthedocs.io/en/stable/manual.html
import csv
import io

from mealymachinemodel.state import State
from mealymachinemodel.transition import Transition


class MealyMachine(object) :
    input_alphabet : tuple
    output_alphabet : tuple
    _name : str
    _states : dict
    _id_initial_state : int
    _transitions: dict #[id:tr,]
    def __init__(self, ia:tuple, oa:tuple, name="mealymachinemodel"):
        self._states={}
        self._transitions={}
        self.input_alphabet = ia
        self.output_alphabet = oa
        self._id_initial_state = -1
        self._name =name

    def get_input_alphabet(self) -> tuple:
        return self.input_alphabet
    
    def get_output_alphabet(self) -> tuple:
        return self.output_alphabet

    def set_name(self,name:str):
        self._name = name

    def get_name(self)->str:
        return self._name

    def __str__(self)->str:
        buffer = io.StringIO()
        for tr in self._transitions.values() :
            buffer.write(f'{tr}\n')
        return buffer.getvalue()

    def _get_next_state_id(self):
        return len(self._states.keys())

    def _get_next_transition_id(self):
        return len(self._transitions.keys())

    def set_initial_state(self, id:int):
        self._id_initial_state = id

    def get_initial_state_id(self) ->int :
        return self._id_initial_state

    def get_initial_state(self)->State:
        return self.get_state(self.get_initial_state_id())

    def get_state(self, id)->State:
        return self._states[id]

    def get_states(self) ->list :
        return self._states.values()

    def add_state(self, etat:State)->State:
        if etat.get_id() == -1 :
            id = self._get_next_state_id()
            etat.set_id(id)
        else :
            id = etat.get_id()
        self._states[id] = etat
        return etat

    def get_transition(self, id:int)->Transition:
        return self._transitions[id]

    def get_transitions(self)->list:
        return self._transitions.values()
    
    def transition_exist(self, Idsrc, input, output, Idtgt)->bool:
        src = self.get_state(Idsrc)
        tgt = self.get_state(Idtgt)
        for tr in self.get_transitions() :
            if tr.get_input() == input and tr.get_output() == output and tr.get_tgt() == tgt :
                return True
        return False

    def complete_with_self_loops(self):
        for etat in self.get_states() :
            for input in self.get_input_alphabet() :
                try :
                    etat.get_out_transition(input)
                except :
                    output = self.get_output_alphabet()[0]
                    self.add_transition(etat.get_id(), input, output, etat.get_id())

    def complete_with_dead_state(self):
        dead_state = self.add_state(State("D"))
        for etat in self.get_states() :
            if etat.get_id() != dead_state.get_id() :
                for input in self.get_input_alphabet() :
                    try :
                        etat.get_out_transition(input)
                    except :
                        output = self.get_output_alphabet()[0]
                        self.add_transition(etat.get_id(), input, output, dead_state.get_id())


    def add_transition(self, idSrc: int, input: str, output:str, idTgt):
        src = self.get_state(idSrc)
        tgt = self.get_state(idTgt)
        #Todo : tester si src et tgt ne sont pas null
        tr = Transition(src,input,output,tgt)
        id = self._get_next_transition_id()
        tr.set_id(id)
        self._transitions[id] = tr
        return tr

    def computeanouputsequence(self, iseq:list) -> tuple:
        rst = [] #list of outputs
        path = [] # list of transitions
        etatcourant = self.get_initial_state()
        for input in iseq :
            transitions = etatcourant.get_out_transition(input)
            if len(transitions) > 0 :
                transition = transitions[0]
                output = transition.get_output()
                rst.append(output)
                path.append(transition.get_id())
                etatcourant = transition.get_tgt()
            else :
                break # il faut lever une exception
        else :
            return rst, path
        return [],[]     
    
    def get_state_of_arrival(self, iseq:list) -> State:
        _, path = self.computeanouputsequence(iseq)
        if len(path) > 0 :
            return self.get_transition(path[-1]).get_tgt()

    def find_a_path_to_one_state_in(self, target_state_ids:set):
        etat_a_visiter = [([],[],self.get_initial_state())]
        etat_deja_visite = set()
        while len(etat_a_visiter) > 0 :
            iseq, path, etat_courant = etat_a_visiter.pop(0)
            etat_deja_visite.add(etat_courant.get_id())
            transitions = etat_courant.get_out_transition()
            for trs in transitions :
                for tr in trs :
                    input = tr.get_input()
                    tgt = tr.get_tgt()
                    if tgt.get_id() not in etat_deja_visite :
                        iseq_new = list(iseq)
                        iseq_new.append(input)
                        path_new = list(path)
                        path_new.append(tr)
                        etat_a_visiter.append((iseq_new,path_new,tgt))
                        if tgt.get_id() in target_state_ids :
                            return iseq_new,path_new
        return [],[]


    def from_csv(self, filename) :
        seen_states = {}
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if row[0] not in seen_states:
                    sid = int(row[0][1:])
                    state = self.add_state(State(row[0], id = sid))
                    seen_states[row[0]] = state.get_id()
                if row[3] not in seen_states:
                    sid = int(row[3][1:])
                    state = self.add_state(State(row[3], id = sid))
                    seen_states[row[3]] = state.get_id()
                self.add_transition(seen_states[row[0]], row[1], row[2], seen_states[row[3]])
        self.set_initial_state(0)
        return self


    def toDot(self) -> str :
        rst =""
        rst+= f'digraph mm' + "{"
        for cle in self._states.keys() :
            rst += "\n\t" + self._states[cle].toDot()

        for cle in self._transitions.keys() :
            rst += "\n\t" + self._transitions[cle].toDot()
        rst+="\n}"
        return rst

    def toNL(self) -> str :
      rst =""
      for cle in self._transitions.keys() :
         rst +=  " "+self._transitions[cle].toNL() + ".\n"
      return rst






