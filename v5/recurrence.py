import mealymachineproduct.productalgorithms as pa


def make_new_prompt(w_m1, w_m2, g_m1, prompt):
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

def make_new_prompt_with_incomplete_io_seq(seq, prompt):
    iseq = ""
    oseq = ""
    for i, o, _ in seq:
        iseq += i
        oseq += o
    new_prompt = prompt
    new_prompt += "Correct the automaton so that this input sequence given to the automaton: \n"
    new_prompt += iseq + "\n"
    new_prompt += "Generates this output sequence: \n"
    new_prompt += oseq + "\n"
    new_prompt += "Please keep this format: State, Input, Output, Next_State, the states should be named Si (where i is always a number), the first row should contain State, Input, Output, Next_State, and the other rows should only contain the state name in Si format (where i is always a number) the input the output and the next state name in Si format (where i is always a number), there shouldnt spaces between each information only comas., here is an example: first row: State, Input, Output, Next_State, second row: S0,a,0,S2 third row: S1,b,1,S3 fourth row: S2,c,0,S1 fifth row: S3,d,1,S0. Do not add any comments \n"
    return new_prompt

def make_new_prompt_with_io_seq(seq, o1, prompt):
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

def make_new_prompt_with_io_seq_list(seq_list, mm1, prompt):
    new_prompt = prompt
    nb_states = len(mm1.get_states())
    print(f"nb_states: {nb_states}")
    max_iter = int(len(seq_list)/nb_states)
    for i in range(max_iter):
        iseq = ""
        oseq = ""
        inp_l = seq_list[i][0]
        out_l = mm1.computeanouputsequence(seq_list[i][0])[0]
        for j in inp_l:
            iseq += j
        for k in out_l:
            oseq += k
        new_prompt += "Correct the automaton so that this input sequence given to the automaton: \n"
        new_prompt += iseq + "\n"
        new_prompt += "Generates this output sequence: \n"
        new_prompt += oseq + "\n"
    new_prompt += "Please keep this format: State, Input, Output, Next_State, the states should be named Si (where i is always a number), the first row should contain State, Input, Output, Next_State, and the other rows should only contain the state name in Si format (where i is always a number) the input the output and the next state name in Si format (where i is always a number), there shouldnt spaces between each information only comas., here is an example: first row: State, Input, Output, Next_State, second row: S0,a,0,S2 third row: S1,b,1,S3 fourth row: S2,c,0,S1 fifth row: S3,d,1,S0. Do not add any comments \n"
    return new_prompt


