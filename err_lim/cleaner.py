# Description: This file contains the functions that clean the generated text and write it to a csv file.
# The prompt is fine-tuned in a way that the format of the generated text is always compatible with the following function as may be seen in the Listing 2 
def write_gen_text_to_csv_file(generated_text):
    res = "" # Initialize the result
    lines = generated_text.split("\n") # Split the generated text by lines
    transitions = [line for line in lines if "S" in line and line.count(",") == 3] # Get the transitions
    with open("generated_text.csv", "w") as f: # Open the csv file
        for transition in transitions: # For each transition
            res += transition + "\n" # Add the transition to the result
            f.write(transition + "\n") # Write the transition to the csv file
    return res # Return the result