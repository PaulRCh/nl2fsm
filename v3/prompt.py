# Description: This file contains the functions to generate the prompt for the user to solve. It also contains the function to get the user input.

import random

import mealymachinegenerator.generatedescription as gd
import mealymachinegenerator.generatormm as gm
import model as mdl

# Generate an automaton prompt

def generate_automaton_prompt(nbState):
    mm = gm.generaterandommm(nbState)
    nl = gd.generatedescription(mm)
    return mm, mm.toDot(), nl

def generate_automaton_prompt_with_random_nb_states():
    nbState = random.randrange(6,15)
    return generate_automaton_prompt(nbState)

def nl_to_prompt(nl):
    return f"{nl} Can you create the previous automaton on csv format with the following order: State, Input, Output, Next_State, the states should be named Si (where i is always a number), the first row should contain State, Input, Output, Next_State, and the other rows should only contain the state name in Si format (where i is always a number) the input the output and the next state name in Si format (where i is always a number), there shouldnt spaces between each information only comas., here is an example: first row: State, Input, Output, Next_State, second row: S0,a,0,S2 third row: S1,b,1,S3 fourth row: S2,c,0,S1 fifth row: S3,d,1,S0. Please do not add any comments to the csv file."

def nl_to_prompt2(nl):
    return f"{nl} In this machine the initial state is 0. If I give the input baab to the machine do I get the following output: 1101? If not, what is the output?"

def get_user_input():
    return input("Please enter a description of an automaton or press enter to generate a random one: ")

def generate_prompt_with_ml(nbState):
    mm = gm.generaterandommm(nbState)
    strmm = str(mm)
    loc_prompt = "Create a natural language description of the automaton below: \n" + strmm
    prompt = mdl.generate_text(loc_prompt)
    return prompt, mm

