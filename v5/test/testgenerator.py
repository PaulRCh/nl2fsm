from mealymachinegenerator.generatormm import *
from mealymachinegenerator.generatedescription import generatedescription
from display.affichage import show_mealy_machine
from random import choice

import os


def testGenerateAndSaveFsmWithDescription(ia=('a','b'), oa=('0','1')) :
   #cwd = os.getcwd()  # Get the current working directory (cwd)
   #files = os.listdir(cwd)  # Get all the files in that directory
   #print("Files in %r: %s" % (cwd, files))
    #buildExampleFsm()

   for k in range(1, 11):
      nbetat = choice(range(1,8))
      fsm = generateinputcompletemm(ia,oa,nbetat)
      os.makedirs(f"./data/exemple{k}",exist_ok=True)
      f = open(f"./data/exemple{k}/fsm.dot", "w")
      f.write(fsm.toDot())
      f.close()
      for i in range(1,10) :
          r= open(f"./data/exemple{k}/requirement{i}.txt", "w")
          r.write(fsm.toNL())
          r.close()

if __name__ == "__main__":
    ia =('a','b')
    oa =('0','1')
    nbetat = choice(range(1,8))
    mm = generateinputcompletemm(ia,oa,nbetat)
    print(mm.toDot())
    print("\n Voici une description \n")
    print(mm.toNL())
    show_mealy_machine(mm)
    print("Voici une trace \n")
    print(generate_trace(mm,4))
    print("\n Voici une description \n")
    print(generatedescription(mm))
    testGenerateAndSaveFsmWithDescription()
