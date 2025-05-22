# utils/openai_utils.py
from dotenv import load_dotenv
from utils.prompts import system_prompt
import os
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

# Function to generate outputs from OpenAI's API
def generate_step_output(prompt, tools=[]):
    
    response = client.responses.create(
        model = "o4-mini",
        reasoning = {"effort": "medium"},
        input = prompt,
        tools = tools,
    )
    
    print("Result:\n")
    print(response.output_text + "\n")
    return response.output_text
