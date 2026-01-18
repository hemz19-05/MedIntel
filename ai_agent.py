import os
from openai import OpenAI
from dotenv import load_dotenv
import random

def assign_variant():
    return random.choice(["A", "B"])

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_response(user_input, context):
    variant = assign_variant()

    if variant == "A":
        style_instruction = (
            "Give a short, concise explanation in simple language. "
            "Use bullet points if helpful."
        )
    else:
        style_instruction = (
            "Give a detailed explanation including mechanism of action, "
            "common uses, and safety considerations."
        )

    system_prompt = f"""
    You are MedIntel, a medical information assistant.
    {style_instruction}
    Always include a medical disclaimer.
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"{user_input}\n\nFDA context:\n{context}"}
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    answer = response.choices[0].message.content

    return answer, variant




