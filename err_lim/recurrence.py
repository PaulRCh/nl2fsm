import mealymachineproduct.productalgorithms as pa

# Function to generate a new prompt based on the errors

def make_new_prompt(w_m1, w_m2, g_m1, prompt): # Generate a new prompt based on the errors
    new_prompt = prompt # Initialize the new prompt with the old prompt
    new_prompt += "Correct the automaton so that these transitions are present in the generated automaton: \n" # Add a message to the new prompt
    for tr in w_m1: # For each desired transition in the oracle automaton
        new_prompt += tr.toNL() + "\n" # Add the transition to the new prompt
    new_prompt += "Correct the automaton so that these transitions are not present in the generated automaton: \n" # Add a message to the new prompt
    for tr in w_m2: # For each undesired transition in the generated automaton
        new_prompt += tr.toNL() + "\n" # Add the transition to the new prompt
    new_prompt += "These transitions are correct and should be present in the generated automaton: \n" # Add a message to the new prompt
    for tr in g_m1: # For each correct transition in the generated automaton
        new_prompt += tr.toNL() + "\n" # Add the transition to the new prompt
    new_prompt += "Please keep this format: State, Input, Output, Next_State, the states should be named Si (where i is always a number), the first row should contain State, Input, Output, Next_State, and the other rows should only contain the state name in Si format (where i is always a number) the input the output and the next state name in Si format (where i is always a number), there shouldnt spaces between each information only comas., here is an example: first row: State, Input, Output, Next_State, second row: S0,a,0,S2 third row: S1,b,1,S3 fourth row: S2,c,0,S1 fifth row: S3,d,1,S0. Do not add any comments \n"
    # Add a message to the new prompt
    return new_prompt # Return the new prompt
