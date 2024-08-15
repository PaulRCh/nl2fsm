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
    mm1, _, nl = prt.generate_automaton_prompt(nbStates) # Generate automaton prompt, returns the automaton mm1 and the natural language description nl
    mm1.set_name("original") # Set the name of the automaton
    dis.show_mealy_machine(mm1) # Display the automaton in repertoire-sortie directory
    prompt = prt.nl_to_prompt(nl) # Convert the natural language description to a prompt
    maximum_iterations = len(mm1.get_states()) * len(mm1.get_input_alphabet()) # Calculate the maximum number of iterations for the correction algorithm
    return prompt, mm1, maximum_iterations # Return the prompt, the automaton and the maximum number of iterations

# Function to generate text based on the prompt and characterize the errors

def err_car(prompt, mm1):
    print("Machine")
    generated_text = mdl.generate_text(prompt) # Generate text based on the prompt using LLM
    cln.write_gen_text_to_csv_file(generated_text) # Write the generated text to a csv file "generated_text.csv"
    ia = mm1.get_input_alphabet() # Get the input alphabet of the automaton
    oa = mm1.get_output_alphabet() # Get the output alphabet of the automaton
    mm2 = mm.MealyMachine(ia,oa) # Create a new automaton
    mm2.from_csv("generated_text.csv") # Load the generated text to the automaton
    mm2.set_name(f"generated") # Set the name of the automaton
    dis.show_mealy_machine(mm2) # Display the automaton in repertoire-sortie directory
    product = pa.ProductMealyMachine(mm1,mm2) # Create a product automaton
    w_m1, w_m2 = product.get_wrong_transitions() # Get the wrong transitions in the generated automaton
    g_m1 = product.get_good_transitions() # Get the correct transitions in the generated automaton
    correct_size = len(g_m1) # Get the number of correct transitions
    if len(w_m1) != 0 or len(w_m2) != 0: # If there are wrong transitions
        err1, err2, err3, err4 = product.caracterize_errors() # Characterize the errors
        print(f"Errors: \n")
        print(f"Type 1 errors (non-deterministic machine generated): {err1} \n")
        print(f"Type 2 errors (non-complete machine generated): {err2} \n")
        print(f"Type 3 errors (output diff): {err3} \n")
        print(f"Type 4 errors (target state diff): {err4} \n")
        print(f"Correct transitions: {correct_size} \n")
        return err1, err2, err3, err4, correct_size # Return the errors
    else: # If there are no wrong transitions
        print("Machine is correct! \n")
        return 0, 0, 0, 0, correct_size # Return 0 for all errors

# Function to characterize the errors

def error_caracterization(nbstates):
    err1_moy = 0 # Initialize the mean error 1
    err2_moy = 0 # Initialize the mean error 2
    err3_moy = 0 # Initialize the mean error 3
    err4_moy = 0 # Initialize the mean error 4
    c_tran_moy = 0 # Initialize the mean correct transitions
    moy_err = 0 # Initialize the mean error
    max_err1 = 0 # Initialize the max error 1
    max_err2 = 0 # Initialize the max error 2
    max_err3 = 0 # Initialize the max error 3
    max_err4 = 0 # Initialize the max error 4
    max_c_tran = 0 # Initialize the max correct transitions
    max_global_err = 0 # Initialize the max global error
    for i in range(30): # Run the error characterization 30 times
        prpt, mm1, _= generate_automaton_prompt(nbstates) # Generate an automaton prompt
        err1, err2, err3, err4, c_tran = err_car(prpt, mm1) # Characterize the errors
        total_err = err1 + err2 + err3 + err4 # Calculate the total error
        err1_moy += err1 # Add the error 1 to the mean error 1
        err2_moy += err2 # Add the error 2 to the mean error 2
        err3_moy += err3 # Add the error 3 to the mean error 3
        err4_moy += err4 # Add the error 4 to the mean error 4
        moy_err += total_err # Add the total error to the mean error
        c_tran_moy += c_tran # Add the correct transitions to the mean correct transitions
        if err1 > max_err1: # Update the max error 1
            max_err1 = err1 
        if err2 > max_err2: # Update the max error 2
            max_err2 = err2
        if err3 > max_err3: # Update the max error 3
            max_err3 = err3
        if err4 > max_err4: # Update the max error 4
            max_err4 = err4
        if c_tran > max_c_tran: # Update the max correct transitions
            max_c_tran = c_tran
        if total_err > max_global_err: # Update the max global error
            max_global_err = total_err
    moy_err = moy_err/30 # Calculate the mean error
    err1_moy = err1_moy/30 # Calculate the mean error 1
    err2_moy = err2_moy/30 # Calculate the mean error 2
    err3_moy = err3_moy/30 # Calculate the mean error 3
    err4_moy = err4_moy/30 # Calculate the mean error 4
    c_tran_moy = c_tran_moy/30 # Calculate the mean correct transitions
    return moy_err, err1_moy, err2_moy, err3_moy, err4_moy, c_tran_moy, max_err1, max_err2, max_err3, max_err4, max_c_tran, max_global_err # Return the mean error, mean errors, mean correct transitions, max errors, max correct transitions and max global error
    


# Main function to run the pipeline

def main():
        dir_path = "repertoire-sortie" # Set the directory path
        if os.path.exists(dir_path): # If the directory exists
            shutil.rmtree(dir_path) # Remove the directory
        os.makedirs(dir_path, exist_ok=True) # Create the directory
        # prpt, mm1, _ = generate_automaton_prompt(10)
        # err_car(prpt, mm1)
        moy_err, err1_moy1, err2_moy1, err3_moy1, err4_moy1, c_tran_moy1, max_err1, max_err2, max_err3, max_err4, max_c_tran, max_global_err = error_caracterization(5) # Characterize the errors for 5 states automaton
        with open("errors1.txt", "w") as f: # Write the errors to a file
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
        moy_err, err1_moy2, err2_moy2, err3_moy2, err4_moy2, c_tran_moy2, max_err1, max_err2, max_err3, max_err4, max_c_tran, max_global_err = error_caracterization(10) # Characterize the errors for 10 states automaton
        with open("errors2.txt", "w") as f: # Write the errors to a file
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