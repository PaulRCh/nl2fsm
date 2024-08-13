import graphviz

from mealymachinemodel.mealymachine import MealyMachine
from mealymachineproduct.productalgorithms import *


def show_mealy_machine(mm:MealyMachine) :
    dot = graphviz.Digraph(mm.get_name(), format='png')
    for etat in mm.get_states() :
        diff = False
        if isinstance(mm, ProductMealyMachine) :
            diff = etat.get_id() in mm.diff_states_id
        if not diff :
            dot.node(f's{etat.get_id()}', f's{etat.get_id()}({etat.get_name()})')
        else :
            dot.node(f's{etat.get_id()}', f's{etat.get_id()}({etat.get_name()})', style='filled', fillcolor='red')
    for tr in mm.get_transitions() :
        dot.edge(f's{tr.get_src().get_id()}',
                 f's{tr.get_tgt().get_id()}',
                 tr.get_input()+'/'+tr.get_output())

    dot.render(directory='repertoire-sortie', view=False)

