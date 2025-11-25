from google.genai import Client

class GeminiLLM:
    def __init__(self, api_key: str):
        # Correct way to initialize the client
        self.client = Client(api_key=api_key)
        self.model = "gemini-flash-latest"   # Valid model from your list

    def summarize(self, text: str):
        prompt = f"Summarize this text in 1–2 sentences:\n{text}"

        res = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        return res.text

    def extract_tasks(self, text: str):
        prompt = f"""
Extract clear action items from the following text.
Return ONLY a Python list of strings.

Text:
{text}
"""

        res = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        # Try to parse Python list returned by LLM
        try:
            return eval(res.text)
        except Exception:
            # fallback simple extraction
            tasks = []
            for line in text.splitlines():
                clean = line.strip()
                if clean.startswith("-") or clean.startswith("*"):
                    tasks.append(clean)
            return tasks
