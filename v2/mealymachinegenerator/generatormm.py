import random

from display import affichage
from mealymachinemodel.mealymachine import MealyMachine
from mealymachinemodel.state import State


def generateinputcompletemm(ia:list, oa:list, nb_etats=4)->MealyMachine :
    mm = MealyMachine(tuple(ia),tuple(oa))
    #ajout des états
    etats=[]
    non_input_complete_states = []
    #print(non_input_complete_states)
    for i in range(0,nb_etats):
        non_input_complete_states.append(i)
        etats.append(mm.add_state(State(name = f'S{i}')))
    mm.set_initial_state(0)
    # construire une sous machine accessible
    # seul l'état 0 est accessible au départ
    reachable=[0]
    while (len(reachable)<nb_etats) :
        available_src = [x for x in reachable if x in non_input_complete_states]
        id_src = random.choice(available_src)
        used_input = mm.get_state(id_src).get_defined_input()
        unused_input = [a for a in ia if a not in used_input]
        print(id_src, unused_input)
        input=random.choice(unused_input)
        output=random.choice(oa)
        available_tgt = [x for x in range(0,nb_etats) if x not in reachable]
        id_tgt = random.choice(available_tgt) #range(0,nb_etats))
        print(f'{id_src},{input},{output},{id_tgt}')
        mm.add_transition(id_src,input,output,id_tgt)
        # mise à jour
        if (len(unused_input)<=1) :
            non_input_complete_states.remove(id_src)
        if id_src in reachable :
            reachable.append(id_tgt)
    ## ajout des autres transitions
    print("non input complete",non_input_complete_states)
    while (len(non_input_complete_states)>0):
        id_src = random.choice(non_input_complete_states)
        used_input = mm.get_state(id_src).get_defined_input()
        unused_input = [a for a in ia if a not in used_input]
        input=random.choice(unused_input)
        output=random.choice(oa)
        id_tgt = random.choice(range(0,nb_etats))
        print(f'{id_src},{input},{output},{id_tgt}')
        mm.add_transition(id_src,input,output,id_tgt)
        # mise à jour
        if (len(unused_input)<=1) :
            non_input_complete_states.remove(id_src)
    ##
    return mm

def generaterandommm(nb_etats=4)->MealyMachine :
    ia =['a','b']
    oa =['0','1']
    return generateinputcompletemm(ia, oa, nb_etats)

def generate_trace(mm: MealyMachine, longueur:int) ->list :
    #generate une trace de longeur sous la forme
    # d'une liste de 'i/o'
    rst = list()
    etat_courant = mm.get_state(mm.get_initial_state_id())
    while (len(rst)<longueur) :
        input =  random.choice(etat_courant.get_defined_input())
        transitions = etat_courant.get_out_transition(input)
        transition = random.choice(transitions)
        rst.append(f'{transition.get_input()}/{transition.get_output()}')
        etat_courant = transition.get_tgt()
    return rst



if __name__ == "__main__":
    ia =['a','b']
    oa =['0','1']
    mm = generateinputcompletemm(ia, oa)
    affichage.show_mealy_machine(mm)
    print(generate_trace(mm,5))
