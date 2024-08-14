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
import sat as sat

# Main function to generate an automaton prompt and generate text

def generate_automaton_prompt(nbStates):
    mm1, _, nl = prt.generate_automaton_prompt(nbStates)
    mm1.set_name("original")
    dis.show_mealy_machine(mm1)
    prompt = prt.nl_to_prompt(nl)
    maximum_iterations = len(mm1.get_states()) * len(mm1.get_input_alphabet())
    return prompt, mm1, maximum_iterations

# Pipeline function

def correction_pipeline(prompt, mm1, max_iter, cpt=0):
    print(f"Machine %d \n" % cpt)
    generated_text = mdl.generate_text(prompt)
    cln.write_gen_text_to_csv_file(generated_text)
    ia = mm1.get_input_alphabet()
    oa = mm1.get_output_alphabet()
    mm2 = mm.MealyMachine(ia,oa)
    mm2.from_csv("generated_text.csv")
    mm2.complete_with_self_loops()
    mm2.set_name(f"generated {cpt}")
    dis.show_mealy_machine(mm2)
    #print("product of the two machines \n")
    product = pa.ProductMealyMachine(mm1,mm2)
    code, mm3 = product.make_product()
    # #print("product done \n")
    print("producing checking sequence \n")
    check_seq = sat.checking_sequence(mm2)
    print("checking sequence done \n")
    print("extracting input and output sequences \n")
    input_seq = sat.extract_input_sequence_from_trace(check_seq)
    output_seq_mm2 = sat.extract_output_sequence_from_trace(check_seq)
    output_seq_mm1 = mm1.computeanouputsequence(input_seq)[0]
    print("input and output sequences extracted \n")
    #output_seq_user = prt.get_user_input_for_check(check_seq)
    if code == 0:
        #print("evaluating the product \n")
        mm3.set_name("product")
        #print("finding a path to a diff state")
        diff_paths = mm3.find_a_path_to_all_diff_states()
        if diff_paths == [] and output_seq_mm1 == output_seq_mm2: #both tests are equivalent (diff_path is used for security purposes)
            dis.show_mealy_machine(mm3)
            print("Machine is correct! \n")
            return cpt
        else:
            np = rec.make_new_prompt_with_io_seq(input_seq, output_seq_mm1, prompt)
            print(f"new prompt: {np}\n")
            if cpt == max_iter:
                return -1
            return correction_pipeline(np, mm1, max_iter, cpt+1)
    else:
        assert(False)

# Benchmark functions

def correction_benchmark(nbstates):
    score = {}
    for i in range(10):
        dir_path = "repertoire-sortie"
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        os.makedirs(dir_path, exist_ok=True)
        print(f"Machine %d \n" % i)
        prompt, mm1, max_iter = generate_automaton_prompt(nbstates)
        iternum = correction_pipeline(prompt, mm1, max_iter)
        print(iternum)
        if iternum in score:
            score[iternum] += 1
        else:
            score[iternum] = 1
    return score    

# Main function to run the pipeline

def main():
    dir_path = "repertoire-sortie"
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.makedirs(dir_path, exist_ok=True)
    # prpt, mm1, max_iter = generate_automaton_prompt(5)
    # correction_pipeline(prpt, mm1, max_iter)
    scores1 = correction_benchmark(5)
    with open("scores1.txt", "w") as f:
        f.write("Scores for 5 states: \n")
        for key in scores1:
            print(key)
            if key == -1:
                f.write(f"{scores1[key]} machines were not corrected \n")
            else:
                f.write(f"corrected in {key} iterations: {scores1[key]} \n")
    # scores2 = correction_benchmark(10)
    # with open("scores2.txt", "w") as f:
    #     f.write("Scores for 10 states: \n")
    #     for key in scores2:
    #         if key == -1:
    #             f.write(f"{scores2[key]} machines were not corrected \n")
    #         else:
    #             f.write(f"corrected in {key} iterations: {scores2[key]} \n") 
main()