# Install the required libraries
# pip install transformers

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Use '3' to suppress all logs

# Disable oneDNN optimizations
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# Use GPT-2 as a free alternative
model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Create a text-generation pipeline
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

def generate_game_idea(prompt):
    """
    Generate a game idea using a free model.
    :param prompt: A string describing the type of game idea you want.
    :return: A string containing the generated game idea.
    """
    try:
        response = generator(prompt, max_length=200, num_return_sequences=1)
        return response[0]["generated_text"]
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__": 
    user_prompt = "Generate a game idea for a Halloween-themed party game."
    game_idea = generate_game_idea(user_prompt)
    print(game_idea)