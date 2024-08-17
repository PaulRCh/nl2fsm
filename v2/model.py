# Description: This file contains the code to generate text using the OpenAI GPT-3.5-turbo model. The model is used to generate a CSV representation of a finite state machine (FSM) from a natural language description.

# the commented lines allow the usage of the llama metha models, note that if you want to use a different version of llama you can change the model name in the commented lines, the uncommented lines are for the openai gpt-3.5-turbo model
# gpt-3.5-turbo is the model that is being used in this project due to lack of calculation power of personal computers, local usage of models such as llama should be done with supercalculators or cloud services

# import torch
# import torch.nn as nn
import os

from dotenv import load_dotenv
from openai import OpenAI

# from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer

load_dotenv()

# Load the model

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()


message_history = []

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-hf", device_map = "auto", token= "") Please add hf token to use llama models

# tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf", token= "") Please add hf token to use llama models

# Generate text with the model

def generate_text(prompt):
    global message_history
    if len(message_history) == 0:
        message_history.append({"role": "system", "content": "You are a professional software engineer working on a project to generate a CSV representation of a finite state machine (FSM) from a natural language description. You have been given the following description:"})
    message_history.append({"role": "user", "content": prompt})
    # print("Generating text...")
    # input_ids = tokenizer(prompt, return_tensors="pt").to(device)
    # print("generated tokens...")
    # output = model.generate(**input_ids, max_new_tokens=10, do_sample=True, temperature=0.6, top_p=0.9)
    # print("generated text...")
    # return tokenizer.decode(output[0], skip_special_tokens=True)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.0,
        messages=message_history,
    )
    message_history.append({"role": "system", "content": response.choices[0].message.content})
    # for message in message_history:
    #     print(message)
    return response.choices[0].message.content