from dotenv import load_dotenv
import os

from groq import APIError
from tui_ai.core.config import CONFIG_DB
from tui_ai.util.file_handing import load_json
from tui_ai.AI.online import gemini_response, groq_response
load_dotenv()
data=load_json(CONFIG_DB)
model_name=data["model"]
provider_name=data["provider"]
gemini_key=os.getenv("GEMINI_API_KEY")
groq_key=os.getenv("GROQ_API_KEY")
def routing(user_input:str):
    try: 
        if provider_name == "gemini":
            return gemini_response(gemini_model=model_name,api_key=gemini_key,user_input=user_input)
        else:
            return groq_response(groq_model=model_name,api_key=groq_key,user_input=user_input)
    except APIError as e:
        return "API Error: " + str(e)