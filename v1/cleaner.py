# Description: This file contains the functions that clean the generated text and write it to a csv file.

def write_gen_text_to_csv_file(generated_text):
    res = ""
    lines = generated_text.split("\n")
    transitions = [line for line in lines if "S" in line and line.count(",") == 3]
    with open("generated_text.csv", "w") as f:
        for transition in transitions:
            res += transition + "\n"
            f.write(transition + "\n")
    return res