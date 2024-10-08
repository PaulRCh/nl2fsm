# Description: This file contains the code to generate text using the OpenAI GPT's models. The model GPT-4o is used to generate a CSV representation of a finite state machine (FSM) from a natural language description.

# the commented lines allow the usage of the llama metha models, note that if you want to use a different version of llama you can change the model name in the commented lines, the uncommented lines are for the openai gpt-4o model
# gpt-4o is the model that is being used in this project due to lack of calculation power of personal computers, local usage of models such as llama should be done with supercalculators or cloud services

# import torch
# import torch.nn as nn
import os

from dotenv import load_dotenv
from openai import OpenAI

# from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer

load_dotenv() # Load the environment variables

# Load the model

api_key = os.getenv("OPENAI_API_KEY") # Get the OpenAI API key from the environment variables
client = OpenAI() # Create an OpenAI client with the API key

machine_role1 = "You are a professional software engineer working on a project to generate a CSV representation of a finite state machine (FSM) from a natural language description. You have been given the following description:" # Set the role of the machine

machine_role2 = "You are a formal methods worker and you are testing Mealy Machines the following question has been given to you:" # Set the role of the machine
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-hf", device_map = "auto", token= "") Please add hf token to use llama models

# tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf", token= "") Please add hf token to use llama models

# Generate text with the model

def generate_text(prompt):
    # print("Generating text...")
    # input_ids = tokenizer(prompt, return_tensors="pt").to(device)
    # print("generated tokens...")
    # output = model.generate(**input_ids, max_new_tokens=10, do_sample=True, temperature=0.6, top_p=0.9)
    # print("generated text...")
    # return tokenizer.decode(output[0], skip_special_tokens=True)
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.0,
        messages=[
            {"role": "system", "content": machine_role1},
            {"role": "user", "content": prompt},
        ],
    ) # Generate text with the OpenAI model
    return response.choices[0].message.content # Return the generated text