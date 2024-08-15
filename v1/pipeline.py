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

def generate_automaton_prompt(nbStates): # A complete description of this function is present in the err_lim/pipeline.py file
    mm1, _, nl = prt.generate_automaton_prompt(nbStates)
    mm1.set_name("original")
    dis.show_mealy_machine(mm1)
    prompt = prt.nl_to_prompt(nl)
    maximum_iterations = len(mm1.get_states()) * len(mm1.get_input_alphabet())
    return prompt, mm1, maximum_iterations

# Pipeline function

def correction_pipeline(prompt, mm1, max_iter, cpt=0): # Function to generate and correct the automaton if needed
    print(f"Machine %d \n" % cpt) # Print the machine number
    generated_text = mdl.generate_text(prompt) # Generate text based on the prompt
    cln.write_gen_text_to_csv_file(generated_text)  # Write the generated text to a csv file
    ia = mm1.get_input_alphabet() # Get the input alphabet of the automaton
    oa = mm1.get_output_alphabet() # Get the output alphabet of the automaton
    mm2 = mm.MealyMachine(ia,oa) # Create a new automaton
    mm2.from_csv("generated_text.csv") # Load the generated text to the automaton
    mm2.set_name(f"generated {cpt}") # Set the name of the automaton
    dis.show_mealy_machine(mm2) # Display the automaton in repertoire-sortie directory
    product = pa.ProductMealyMachine(mm1,mm2) # Create a product automaton
    w_m1, w_m2 = product.get_wrong_transitions() # Get the wrong transitions in the generated automaton
    g_m1 = product.get_good_transitions() # Get the correct transitions in the generated automaton
    if len(w_m1) != 0 or len(w_m2) != 0: # If there are wrong transitions
        print("Machine is incorrect! \n") 
        new_prompt = rec.make_new_prompt(w_m1, w_m2, g_m1, prompt) # Generate a new prompt based on the errors
        #print(new_prompt)
        if cpt == max_iter: # If the maximum number of iterations is reached
            return -1 # Return -1
        return correction_pipeline(new_prompt, mm1, max_iter, cpt+1) # Recursively call the correction pipeline
    else: # If there are no wrong transitions
        print("Machine is correct! \n")
        return cpt # Return the number of iterations

# Benchmark functions

def pipeline_benchmark(nbstates): # Benchmark function for the pipeline
    score = 0 # Initialize the score
    for i in range(30): # For each machine
        print(f"Machine %d \n" % i) # Print the machine number
        mm1, _, nl = prt.generate_automaton_prompt(nbstates) # Generate automaton prompt
        mm1.set_name("original") # Set the name of the automaton
        #dis.show_mealy_machine(mm1)
        prompt = prt.nl_to_prompt(nl) # Convert the natural language description to a prompt
        generated_text = mdl.generate_text(prompt) # Generate text based on the prompt
        cln.write_gen_text_to_csv_file(generated_text) # Write the generated text to a csv file
        ia = mm1.get_input_alphabet() # Get the input alphabet of the automaton
        oa = mm1.get_output_alphabet() # Get the output alphabet of the automaton
        mm2 = mm.MealyMachine(ia,oa) # Create a new automaton
        mm2.from_csv("generated_text.csv") # Load the generated text to the automaton
        mm2.set_name("generated") # Set the name of the automaton
        #dis.show_mealy_machine(mm2)
        product = pa.ProductMealyMachine(mm1,mm2) # Create a product automaton
        code, mm3 = product.make_product() # Make the product automaton
        if code == 0: # If the product automaton is correct
            mm3.set_name("product") # Set the name of the product automaton
            if len(mm3.diff_states_id) != 0: # If there are diff states (states that are reachable only if there is a difference in the output between the oracle and the generated automaton)
                score += 1 # Increment the score
        else: # If the product automaton is incorrect
            score += 1 # Increment the score
    return score # Return the score

def correction_benchmark(nbstates):
    score = {} # Initialize the score
    for i in range(30): # For each machine
        dir_path = "repertoire-sortie" # Set the directory path
        if os.path.exists(dir_path): # If the directory exists
            shutil.rmtree(dir_path) # Remove the directory
        os.makedirs(dir_path, exist_ok=True) # Create the directory (this is only for cleaning the directory, for easy visualization and debugging)
        print(f"Machine %d \n" % i) # Print the machine number
        prompt, mm1, max_iter = generate_automaton_prompt(nbstates) # Generate an automaton prompt
        iternum = correction_pipeline(prompt, mm1, max_iter) # Run the correction pipeline
        print(iternum) # Print the number of iterations
        if iternum in score: # If the number of iterations is in the score
            score[iternum] += 1 # Increment the score
        else: # If the number of iterations is not in the score
            score[iternum] = 1 # Add the number of iterations to the score
    return score # Return the score

# Main function to run the pipeline

def main():
        dir_path = "repertoire-sortie"
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        os.makedirs(dir_path, exist_ok=True)
        prpt, mm1, max_iter = generate_automaton_prompt(5)
        correction_pipeline(prpt, mm1, max_iter)
        # correction_pipeline(prpt, mm1)
        # scores1 = correction_benchmark(5)
        # scores2 = correction_benchmark(10)
        # with open("scores1.txt", "w") as f:
        #     f.write("Scores for 5 states: \n")
        #     for key in scores1:
        #         print(key)
        #         if key == -1:
        #             f.write(f"{scores1[key]} machines were not corrected \n")
        #         else:
        #             f.write(f"corrected in {key} iterations: {scores1[key]} \n")
        # with open("scores2.txt", "w") as f:
        #     f.write("Scores for 10 states: \n")
        #     for key in scores2:
        #         if key == -1:
        #             f.write(f"{scores2[key]} machines were not corrected \n")
        #         else:
        #             f.write(f"corrected in {key} iterations: {scores2[key]} \n") (commented lines allow running and writing the benchmark results to a file)    
main()