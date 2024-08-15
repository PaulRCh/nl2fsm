import mealymachineproduct.productalgorithms as pa


def make_new_prompt(w_m1, w_m2, g_m1, prompt): # This function is not used in the current version of the code
    new_prompt = prompt
    new_prompt += "Correct the automaton so that these transitions are present in the generated automaton: \n"
    for tr in w_m1:
        new_prompt += tr.toNL() + "\n"
    new_prompt += "Correct the automaton so that these transitions are not present in the generated automaton: \n"
    for tr in w_m2:
        new_prompt += tr.toNL() + "\n"
    new_prompt += "These transitions are correct and should be present in the generated automaton: \n"
    for tr in g_m1:
        new_prompt += tr.toNL() + "\n"
    new_prompt += "Please keep this format: State, Input, Output, Next_State, the states should be named Si (where i is always a number), the first row should contain State, Input, Output, Next_State, and the other rows should only contain the state name in Si format (where i is always a number) the input the output and the next state name in Si format (where i is always a number), there shouldnt spaces between each information only comas., here is an example: first row: State, Input, Output, Next_State, second row: S0,a,0,S2 third row: S1,b,1,S3 fourth row: S2,c,0,S1 fifth row: S3,d,1,S0. Do not add any comments \n"
    return new_prompt

def make_new_prompt_with_incomplete_io_seq(seq, prompt): # Function to generate a new prompt based on the errors (seq is not only the input output sequence, a returned value is ignored)
    iseq = "" # Initialize the input sequence
    oseq = "" # Initialize the output sequence
    for i, o, _ in seq: # For each input, output pair in the sequence
        iseq += i # Add the input to the input sequence
        oseq += o # Add the output to the output sequence
    new_prompt = prompt # Initialize the new prompt with the old prompt
    new_prompt += "Correct the automaton so that this input sequence given to the automaton: \n" # Add a message to the new prompt
    new_prompt += iseq + "\n" # Add the input sequence to the new prompt
    new_prompt += "Generates this output sequence: \n" # Add a message to the new prompt
    new_prompt += oseq + "\n" # Add the output sequence to the new prompt
    new_prompt += "Please keep this format: State, Input, Output, Next_State, the states should be named Si (where i is always a number), the first row should contain State, Input, Output, Next_State, and the other rows should only contain the state name in Si format (where i is always a number) the input the output and the next state name in Si format (where i is always a number), there shouldnt spaces between each information only comas., here is an example: first row: State, Input, Output, Next_State, second row: S0,a,0,S2 third row: S1,b,1,S3 fourth row: S2,c,0,S1 fifth row: S3,d,1,S0. Do not add any comments \n"
    # Add a message to the new prompt
    return new_prompt # Return the new prompt # Return the new prompt

def make_new_prompt_with_io_seq(seq, o1, prompt): # Similar to the previous function but the sequence source is different
    iseq = ""
    oseq = ""
    for i in seq:
        iseq += i
    for o in o1:
        oseq += o
    new_prompt = prompt
    new_prompt += "Correct the automaton so that this input sequence given to the automaton: \n"
    new_prompt += iseq + "\n"
    new_prompt += "Generates this output sequence: \n"
    new_prompt += oseq + "\n"
    new_prompt += "Please keep this format: State, Input, Output, Next_State, the states should be named Si (where i is always a number), the first row should contain State, Input, Output, Next_State, and the other rows should only contain the state name in Si format (where i is always a number) the input the output and the next state name in Si format (where i is always a number), there shouldnt spaces between each information only comas., here is an example: first row: State, Input, Output, Next_State, second row: S0,a,0,S2 third row: S1,b,1,S3 fourth row: S2,c,0,S1 fifth row: S3,d,1,S0. Do not add any comments \n"
    return new_prompt

def make_new_prompt_with_io_seq_list(seq_list, mm1, prompt): # Similar to the previous function but the are multiple sequences
    new_prompt = prompt # Initialize the new prompt with the old prompt
    nb_states = len(mm1.get_states()) # Get the number of states in the automaton
    print(f"nb_states: {nb_states}") # Print the number of states
    max_iter = int(len(seq_list)/nb_states) # Calculate the maximum number of iterations, proportion of sequences we want to keep
    for i in range(max_iter): # For each iteration
        iseq = "" # Initialize the input sequence
        oseq = "" # Initialize the output sequence
        inp_l = seq_list[i][0] # Get the input sequence
        out_l = mm1.computeanouputsequence(seq_list[i][0])[0] # Compute the output sequence
        for j in inp_l: # For each input in the input sequence
            iseq += j # Add the input to the input sequence
        for k in out_l: # For each output in the output sequence
            oseq += k # Add the output to the output sequence
        new_prompt += "Correct the automaton so that this input sequence given to the automaton: \n"
        new_prompt += iseq + "\n"
        new_prompt += "Generates this output sequence: \n"
        new_prompt += oseq + "\n"
    new_prompt += "Please keep this format: State, Input, Output, Next_State, the states should be named Si (where i is always a number), the first row should contain State, Input, Output, Next_State, and the other rows should only contain the state name in Si format (where i is always a number) the input the output and the next state name in Si format (where i is always a number), there shouldnt spaces between each information only comas., here is an example: first row: State, Input, Output, Next_State, second row: S0,a,0,S2 third row: S1,b,1,S3 fourth row: S2,c,0,S1 fifth row: S3,d,1,S0. Do not add any comments \n"
    return new_prompt


