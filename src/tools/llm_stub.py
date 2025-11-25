class LLMStub:
    """
    Very simple stub LLM that simulates behavior.
    Replace this with Gemini later.
    """

    def summarize(self, text: str) -> str:
        # Simple mock summary
        lines = text.splitlines()
        return "Summary: " + (lines[0] if lines else "No content")

    def extract_tasks(self, text: str):
        # Very simple extraction: return all lines starting with "-", "*"
        tasks = []
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("-") or line.startswith("*"):
                tasks.append(line)
        return tasks
