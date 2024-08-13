from mealymachinemodel.mealymachine import MealyMachine
from mealymachinemodel.transition import Transition
from mealymachinemodel.state import State
import random

def generatedescription(mm:MealyMachine) -> str :
        rst =""
        for cle in mm._transitions.keys() :
            rst +=  " "+ transitionToNL(mm._transitions[cle]) + ".\n"
        return rst

def transitionToNL(tr: Transition) -> str :
       liste = [f"{fromtoNL(tr)} {outputtoNL(tr)} and {movetoNL(tr)} {inputtoNL(tr)}",
                f"{outputtoNL(tr)} and {movetoNL(tr)} {inputtoNL(tr)} {fromtoNL(tr)}"]
       rst = random.choice(liste)
       return rst

def systemtoNL(tr:Transition) ->str :
       liste = ["it", "the system", "the application"]
       rst = random.choice(liste)
       return rst

def fromtoNL(tr:Transition) -> str :
        liste = [f"from {statetoNL(tr._src)}",
                 f"from state {statetoNL(tr._src)}",
                 f"in state {statetoNL(tr._src)}",
                 f"in  {statetoNL(tr._src)}",
                 f"when the system is in {statetoNL(tr._src)}",
                 f"when it is in {statetoNL(tr._src)}"]
        rst = random.choice(liste)
        return rst

def movetoNL(tr:Transition) -> str :
        liste = [f"{systemtoNL(tr)} moves to {statetoNL(tr._tgt)}",
                 f"{systemtoNL(tr)} reaches {statetoNL(tr._tgt)}",
                 f"{statetoNL(tr._tgt)} is reached"]
        rst = random.choice(liste)
        return rst

def inputtoNL(tr:Transition) -> str :
        liste= [f"if the input is {tr._input}",
                f"if the input {tr._input} occurs",
                f"if  {tr._input} occurs",
                f"on occurence of input {tr._input}",
                f"on occurence of {tr._input}"]
        rst = random.choice(liste)
        return rst

def outputtoNL(tr:Transition) -> str :
        liste= [f"{systemtoNL(tr)} produces {tr._output}",
                f"{systemtoNL(tr)} returns {tr._output}",
                f", {tr._output} is produced",
                f"the output {tr._output} is produced",
                f", {tr._output} is returned"]
        rst = random.choice(liste)
        return rst

def statetoNL(s:State) ->str :
      descCandidate = [f"state {s._name}",f"{s._name}"]
      rst = random.choice(descCandidate)
      return rst


