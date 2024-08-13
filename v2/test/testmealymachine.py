from display import affichage
from mealymachinemodel.state import State
from mealymachinemodel.transition import Transition
from mealymachinemodel.mealymachine import MealyMachine
from mealymachineproduct import productalgorithms

def test_state() :
     etat1 = State('s1')
     print(etat1)


def test_transition():
     e1 = State('s1')
     e2 = State('s2')
     tr= Transition(e1,'a','b',e2)
     print(e1)
     print(e2)


def build_machine1() -> MealyMachine :
    ia =('a','b')
    oa =('0','1')
    mm = MealyMachine(ia,oa,'machine1')
    e = []
    for i in range(0,3) :
        e.append(mm.add_state(State(f"s{i}")))

    mm.set_initial_state(0)
    mm.add_transition(e[0].get_id(),mm.input_alphabet[0],mm.output_alphabet[0],e[1].get_id())
    mm.add_transition(e[0].get_id(),mm.input_alphabet[1],mm.output_alphabet[0],e[2].get_id())
    mm.add_transition(e[1].get_id(),mm.input_alphabet[0],mm.output_alphabet[0],e[2].get_id())
    mm.add_transition(e[1].get_id(),mm.input_alphabet[1],mm.output_alphabet[0],e[1].get_id())
    mm.add_transition(e[2].get_id(),mm.input_alphabet[0],mm.output_alphabet[0],e[1].get_id())
    mm.add_transition(e[2].get_id(),mm.input_alphabet[1],mm.output_alphabet[0],e[0].get_id())
    return mm

def build_machine2() -> MealyMachine :
    ia =('a','b')
    oa =('0','1')
    mm = MealyMachine(ia,oa,'machine2')
    e = []
    for i in range(0,3) :
        e.append(mm.add_state(State(f"s{i}")))

    mm.set_initial_state(0)
    mm.add_transition(e[0].get_id(),mm.input_alphabet[0],mm.output_alphabet[0],e[1].get_id())
    mm.add_transition(e[0].get_id(),mm.input_alphabet[1],mm.output_alphabet[1],e[1].get_id())
    mm.add_transition(e[1].get_id(),mm.input_alphabet[0],mm.output_alphabet[0],e[2].get_id())
    mm.add_transition(e[1].get_id(),mm.input_alphabet[1],mm.output_alphabet[0],e[1].get_id())
    mm.add_transition(e[2].get_id(),mm.input_alphabet[0],mm.output_alphabet[0],e[1].get_id())
    mm.add_transition(e[2].get_id(),mm.input_alphabet[1],mm.output_alphabet[0],e[0].get_id())
    return mm

def build_oracle() -> MealyMachine :
    ia =('a','b')
    oa =('0','1','2')
    mm = MealyMachine(ia,oa,'machine1')
    e = []
    for i in range(0,4) :
        e.append(mm.add_state(State(f"s{i}")))

    mm.set_initial_state(0)
    mm.add_transition(e[0].get_id(),mm.input_alphabet[0],mm.output_alphabet[0],e[1].get_id())
    mm.add_transition(e[0].get_id(),mm.input_alphabet[1],mm.output_alphabet[0],e[2].get_id())
    mm.add_transition(e[1].get_id(),mm.input_alphabet[0],mm.output_alphabet[0],e[1].get_id())
    mm.add_transition(e[1].get_id(),mm.input_alphabet[1],mm.output_alphabet[1],e[3].get_id())
    mm.add_transition(e[2].get_id(),mm.input_alphabet[0],mm.output_alphabet[0],e[1].get_id())
    mm.add_transition(e[2].get_id(),mm.input_alphabet[1],mm.output_alphabet[2],e[3].get_id())
    mm.add_transition(e[3].get_id(),mm.input_alphabet[0],mm.output_alphabet[0],e[1].get_id())
    mm.add_transition(e[3].get_id(),mm.input_alphabet[1],mm.output_alphabet[0],e[3].get_id())
    return mm

if __name__ == "__main__":
    mm1= build_oracle()
    print(mm1.toDot())
    affichage.show_mealy_machine(mm1)
    iseq = []
    iseq.append('a')
    iseq.append('b')
    oseq, path = mm1.computeanouputsequence(iseq)
    print(oseq)
    print(path)


