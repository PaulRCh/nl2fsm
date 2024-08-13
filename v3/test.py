import os
import shutil

import display.affichage as dis
import prompt as prt


def test_generate_automaton_prompt():
    mm, dot, nl = prt.generate_automaton_prompt(5)
    strmm = str(mm)
    dis.show_mealy_machine(mm)
    print("mm = \n", strmm)

def test_generate_ml_prompt():
    dir_path = "repertoire-sortie"
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.makedirs(dir_path, exist_ok=True)
    prompt, mm = prt.generate_prompt_with_ml(3)
    print("prompt = \n", prompt)
    dis.show_mealy_machine(mm)

def main():
    test_generate_ml_prompt()

main()
