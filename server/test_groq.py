
import os
import openai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("XAI_API_KEY")
print(f"Testing Groq Key with Llama 3.3: {api_key[:10]}...")

if not api_key:
    exit(1)

try:
    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello! Reply with 'Groq Connection Successful'."}
        ]
    )
    print("Response:", response.choices[0].message.content)
except Exception as e:
    print(f"Error: {e}")
