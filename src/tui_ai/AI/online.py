from google import genai
from groq import Groq
import os

def gemini_response(gemini_model:str,api_key,user_input:str):
    try:
        client=genai.Client(api_key=api_key)
        response=client.interactions.create(model=gemini_model,
        input=user_input)
        return response.output_text # pyright: ignore[reportAttributeAccessIssue]
    except Exception as e:
        return f"Error: {str(e)}"

def groq_response(groq_model:str,api_key,user_input:str):
    try:
        client = Groq(api_key=api_key)
        response=client.chat.completions.create(
            model=groq_model,
            messages=[{"role":"user","content":user_input}],)
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"
