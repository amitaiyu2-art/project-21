import config19 
from openai import OpenAI
GROQ_URL = "https://api.groq.com/openai/v1"
MODELS = getattr(config19, "GROQ_MODELS", ["openai/gpt-oss-20b"])
def generate_response(prompt:str, temperature: float = 0.3, max_tokens: int = 512)->str:
    key = getattr(config19, "GROQ_API_KEY", None)
    if not key:
        return "ERror, GROQ_API_KEY missing in config19.py"
    c = OpenAI(api_key=key, base_url=GROQ_URL)
    last_err = None
    for m in MODELS:
        try:
            r = c.chat.completions.create(
                model=m, 
                messages = [{"role":"user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return r.choices[0].message.content
        except Exception as e:
            last_err = e
    return ("Groq model failed.\n"
            f"Tried models: {MODELS}\n"
            "1) Switch to hf by importing hf.py in main.py OR\n 2) Replace Groq model in groq.py (GROQ_MODELS).\n"
            f"details: {type(last_err).__name__}: {last_err}"
        )