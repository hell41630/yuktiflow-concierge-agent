from google import genai

with open("secrets/gemini_key.txt") as f:
    key = f.read().strip()

client = genai.Client(api_key=key)

for m in client.models.list():
    print(m.name)
