import os
from typing import Dict
from groq import Groq


class FixGeneratorAgent:
    def __init__(self) -> None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY environment variable is not set.")
        self.client = Groq(api_key=api_key)

    def generate_fix(self, file_path: str, bug: Dict[str, object], file_content: str) -> str:
        system_prompt = (
            "You are an autonomous code repair agent.\n\n"
            "You are given:\n"
            "- File path\n"
            "- Bug type\n"
            "- Line number\n"
            "- Short reason\n"
            "- Full file content\n\n"
            "Fix ONLY the specified issue.\n"
            "Do NOT modify unrelated logic.\n"
            "Preserve formatting exactly as much as possible.\n"
            "Return the ENTIRE corrected file content.\n"
            "Do not omit any existing code.\n"
            "Do not summarize.\n"
            "Do not truncate.\n"
            "Return only raw code.\n"
            "No markdown.\n"
            "No explanations.\n"
        )

        file_value = bug.get("file")
        line_value = bug.get("line")
        bug_type_value = bug.get("bug_type")
        short_reason_value = bug.get("short_reason")

        bug_block = (
            f"Target file: {file_path}\n"
            f"Reported file: {file_value}\n"
            f"Line: {line_value}\n"
            f"Bug type: {bug_type_value}\n"
            f"Reason: {short_reason_value}\n"
        )

        user_prompt = (
            f"{bug_block}\n"
            "Current file content:\n\n"
            f"{file_content}"
        )

        try:
            completion = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0,
            )

            content = completion.choices[0].message.content

        except Exception:
            # If API fails, return original file content safely
            return file_content

        if not isinstance(content, str):
            return file_content

        content = content.strip()


        if content.startswith("```"):
            content = (
                content.replace("```python", "")
                .replace("```", "")
                .strip()
            )

        if not content:
            return file_content

        return content
