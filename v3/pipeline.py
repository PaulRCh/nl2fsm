# This file is not commented, because this version is not used nor efficient.

import os
import shutil

import cleaner as cln
import display.affichage as dis
import mealymachinemodel.mealymachine as mm
import mealymachineproduct.productalgorithms as pa
import model as mdl
import prompt as prt
import recurrence as rec

# Main function to generate an automaton prompt and generate text

def generate_automaton_prompt(nbStates):
    prpt, mm1 = prt.generate_prompt_with_ml(nbStates)
    mm1.set_name("original")
    dis.show_mealy_machine(mm1)
    prompt = prt.nl_to_prompt(prpt)
    return prompt, mm1

# Pipeline functions

def correction_pipeline(prompt, mm1, cpt=0):
    print(f"Machine %d \n" % cpt)
    generated_text = mdl.generate_text(prompt)
    cln.write_gen_text_to_csv_file(generated_text)
    ia = mm1.get_input_alphabet()
    oa = mm1.get_output_alphabet()
    mm2 = mm.MealyMachine(ia,oa)
    mm2.from_csv("generated_text.csv")
    mm2.set_name(f"generated {cpt}")
    dis.show_mealy_machine(mm2)
    product = pa.ProductMealyMachine(mm1,mm2)
    try:
        mm3 = product.make_product()
        mm3.set_name("product")
        dis.show_mealy_machine(mm3)
    except:
        print("")
    w_m1, w_m2 = product.get_wrong_transitions()
    g_m1 = product.get_good_transitions()
    if len(w_m1) != 0 or len(w_m2) != 0:
        print("Machine is incorrect! \n")
        new_prompt = rec.make_new_prompt(w_m1, w_m2, g_m1, prompt)
        print(new_prompt)
        if cpt == 20:
            return False
        correction_pipeline(new_prompt, mm1, cpt+1)
    else:
        print("Machine is correct! \n")
        return True

# Benchmark functions

def pipeline_benchmark(nbstates):
    score = 0
    for i in range(100):
        print(f"Machine %d \n" % i)
        mm1, _, nl = prt.generate_automaton_prompt(nbstates)
        mm1.set_name("original")
        #dis.show_mealy_machine(mm1)
        prompt = prt.nl_to_prompt(nl)
        generated_text = mdl.generate_text(prompt)
        cln.write_gen_text_to_csv_file(generated_text)
        ia = mm1.get_input_alphabet()
        oa = mm1.get_output_alphabet()
        mm2 = mm.MealyMachine(ia,oa)
        mm2.from_csv("generated_text.csv")
        mm2.set_name("generated")
        #dis.show_mealy_machine(mm2)
        product = pa.ProductMealyMachine(mm1,mm2)
        try:
            mm3 = product.make_product()
            mm3.set_name("product")
            #dis.show_mealy_machine(mm3)
            if len(mm3.diff_states_id) != 0:
                    score += 1
        except:
            score += 1
    return score

def correction_benchmark(nbstates):
    score = 0
    for i in range(50):
        dir_path = "repertoire-sortie"
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        os.makedirs(dir_path, exist_ok=True)
        print(f"Machine %d \n" % i)
        prompt, mm1 = generate_automaton_prompt(nbstates)
        corrected = correction_pipeline(prompt, mm1)
        if not corrected:
            score += 1
    return score   

# Main function to run the pipeline

def main():
        dir_path = "repertoire-sortie"
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        os.makedirs(dir_path, exist_ok=True)
        prpt, mm1 = generate_automaton_prompt(15)
        corrected = correction_pipeline(prpt, mm1)
main()