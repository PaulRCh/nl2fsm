# Description: This file is the main file to run the pipeline. It generates an automaton prompt and generates text based on the prompt. The text is then cleaned and written to a csv file.

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
    mm1, _, nl = prt.generate_automaton_prompt(nbStates)
    mm1.set_name("original")
    dis.show_mealy_machine(mm1)
    prompt = prt.nl_to_prompt(nl)
    maximum_iterations = len(mm1.get_states()) * len(mm1.get_input_alphabet())
    return prompt, mm1, maximum_iterations

# Function to generate text based on the prompt and characterize the errors

def err_car(prompt, mm1):
    print("Machine")
    generated_text = mdl.generate_text(prompt)
    cln.write_gen_text_to_csv_file(generated_text)
    ia = mm1.get_input_alphabet()
    oa = mm1.get_output_alphabet()
    mm2 = mm.MealyMachine(ia,oa)
    mm2.from_csv("generated_text.csv")
    mm2.set_name(f"generated")
    dis.show_mealy_machine(mm2)
    product = pa.ProductMealyMachine(mm1,mm2)
    w_m1, w_m2 = product.get_wrong_transitions()
    g_m1 = product.get_good_transitions()
    correct_size = len(g_m1)
    if len(w_m1) != 0 or len(w_m2) != 0:
        err1, err2, err3, err4 = product.caracterize_errors()
        print(f"Errors: \n")
        print(f"Type 1 errors (non-deterministic machine generated): {err1} \n")
        print(f"Type 2 errors (non-complete machine generated): {err2} \n")
        print(f"Type 3 errors (output diff): {err3} \n")
        print(f"Type 4 errors (target state diff): {err4} \n")
        print(f"Correct transitions: {correct_size} \n")
        return err1, err2, err3, err4, correct_size
    else:
        print("Machine is correct! \n")
        return 0, 0, 0, 0, correct_size

# Function to characterize the errors

def error_caracterization(nbstates):
    err1_moy = 0
    err2_moy = 0
    err3_moy = 0
    err4_moy = 0
    c_tran_moy = 0
    moy_err = 0
    max_err1 = 0
    max_err2 = 0
    max_err3 = 0
    max_err4 = 0
    max_c_tran = 0
    max_global_err = 0
    for i in range(30):
        prpt, mm1, _= generate_automaton_prompt(nbstates)
        err1, err2, err3, err4, c_tran = err_car(prpt, mm1)
        total_err = err1 + err2 + err3 + err4
        err1_moy += err1
        err2_moy += err2
        err3_moy += err3
        err4_moy += err4
        moy_err += total_err
        c_tran_moy += c_tran
        if err1 > max_err1:
            max_err1 = err1
        if err2 > max_err2:
            max_err2 = err2
        if err3 > max_err3:
            max_err3 = err3
        if err4 > max_err4:
            max_err4 = err4
        if c_tran > max_c_tran:
            max_c_tran = c_tran
        if total_err > max_global_err:
            max_global_err = total_err
    moy_err = moy_err/30
    err1_moy = err1_moy/30
    err2_moy = err2_moy/30
    err3_moy = err3_moy/30
    err4_moy = err4_moy/30
    c_tran_moy = c_tran_moy/30
    return moy_err, err1_moy, err2_moy, err3_moy, err4_moy, c_tran_moy, max_err1, max_err2, max_err3, max_err4, max_c_tran, max_global_err
    


# Main function to run the pipeline

def main():
        dir_path = "repertoire-sortie"
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        os.makedirs(dir_path, exist_ok=True)
        # prpt, mm1, _ = generate_automaton_prompt(10)
        # err_car(prpt, mm1)
        moy_err, err1_moy1, err2_moy1, err3_moy1, err4_moy1, c_tran_moy1, max_err1, max_err2, max_err3, max_err4, max_c_tran, max_global_err = error_caracterization(5)
        with open("errors1.txt", "w") as f:
            f.write(f"Error 1 mean (non-deterministic gen): {err1_moy1} \n")
            f.write(f"Error 2 mean (input diff, missing transition gen): {err2_moy1} \n")
            f.write(f"Error 3 mean (output diff): {err3_moy1} \n")
            f.write(f"Error 4 mean (target state diff): {err4_moy1} \n")
            f.write(f"Correct transitions mean: {c_tran_moy1} \n")
            f.write(f"Max error 1: {max_err1} \n")
            f.write(f"Max error 2: {max_err2} \n")
            f.write(f"Max error 3: {max_err3} \n")
            f.write(f"Max error 4: {max_err4} \n")
            f.write(f"Max correct transitions: {max_c_tran} \n")
            f.write(f"Max global error: {max_global_err} \n")
            f.write(f"Mean error: {moy_err} \n")
        moy_err, err1_moy2, err2_moy2, err3_moy2, err4_moy2, c_tran_moy2, max_err1, max_err2, max_err3, max_err4, max_c_tran, max_global_err = error_caracterization(10)
        with open("errors2.txt", "w") as f:
            f.write(f"Error 1 mean (non-deterministic gen): {err1_moy2} \n")
            f.write(f"Error 2 mean (input diff, missing transition gen): {err2_moy2} \n")
            f.write(f"Error 3 mean (output diff): {err3_moy2} \n")
            f.write(f"Error 4 mean (target state diff): {err4_moy2} \n")
            f.write(f"Correct transitions mean: {c_tran_moy2} \n")
            f.write(f"Max error 1: {max_err1} \n")
            f.write(f"Max error 2: {max_err2} \n")
            f.write(f"Max error 3: {max_err3} \n")
            f.write(f"Max error 4: {max_err4} \n")
            f.write(f"Max correct transitions: {max_c_tran} \n")
            f.write(f"Max global error: {max_global_err} \n")
            f.write(f"Mean error: {moy_err} \n")
     
main()