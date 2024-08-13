# Description: This file is the main file to run the pipeline. It generates an automaton prompt and generates text based on the prompt. The text is then cleaned and written to a csv file.

import copy

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
    return prompt, mm1

def pipeline(prompt, mm1, cpt=0):
    #print(f"og prompt: {og_prompt}")
    print(f"Machine %d in correction\n" % cpt)
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
    g_m2 = product.get_good_transitions()
    # print("Transitions that should be in the machine: \n")
    # for tr in w_m1:
    #     print(tr.toNL())
    #     print("\n")
    # print("Transitions that should not be in the machine: \n")
    # for tr in w_m2:
    #     print(tr.toNL())
    #     print("\n")
    if len(w_m1) != 0 or len(w_m2) != 0:
        print("Machine is incorrect! \n")
        new_prompt = rec.make_new_prompt(w_m1, w_m2, g_m2)
        print(new_prompt)
        if cpt == 20:
            mdl.message_history = []
            return False
        pipeline(new_prompt, mm1, cpt+1)
    else:
        print("Machine is correct! \n")
        mdl.message_history = []
        return True

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
    for i in range(100):
        print(f"Machine test %d \n" % i)
        prompt, mm1 = generate_automaton_prompt(nbstates)
        corrected = pipeline(prompt, mm1)
        if not corrected:
            score += 1
    return score

        

def main():
    # prompt = prt.get_user_input()
    # if prompt == "":
    #     _, _, nl = prt.generate_automaton_prompt_with_random_nb_states()
    #     prompt = prt.nl_to_prompt(nl)
    # sc = pipeline_benchmark(2)
    # print(f"Score: %d/100 bad machines" % sc)
    # prompt, mm1 = generate_automaton_prompt(2)
    # pipeline(prompt, mm1)
    with open("correction_benchmark_score.txt", "w") as file:
        for i in range(4, 6):
            sc = correction_benchmark(i)
            file.write(f"Score: {sc}/100 bad machines for {i} states\n")
main()