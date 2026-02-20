import json
import os
from typing import Any, Dict, List

from groq import Groq


class FailureAnalyzerAgent:
    def __init__(self) -> None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY environment variable is not set.")
        self.client = Groq(api_key=api_key)

    def analyze_failures(self, logs: str) -> List[Dict[str, Any]]:
        system_prompt = (
            "You are a CI failure analyzer.\n\n"
            "Given pytest logs, extract failures.\n\n"
            "Return STRICT JSON array only.\n\n"
            "Each object must contain:\n"
            "- file (string)\n"
            "- line (integer)\n"
            "- bug_type (ONLY from: LINTING, SYNTAX, LOGIC, TYPE_ERROR, IMPORT, INDENTATION)\n"
            "- short_reason (string)\n\n"
            "Return only JSON. No markdown. No explanations."
        )

        user_prompt = f"Here are the CI/test logs:\n\n{logs}\n"

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
            return []

        if not isinstance(content, str):
            return []

        # 🔥 Strip markdown fences if present
        content = content.strip()
        if content.startswith("```"):
            content = content.replace("```json", "").replace("```", "").strip()

        try:
            data = json.loads(content)
        except Exception:
            return []

        if not isinstance(data, list):
            return []

        allowed_bug_types = {
            "LINTING",
            "SYNTAX",
            "LOGIC",
            "TYPE_ERROR",
            "IMPORT",
            "INDENTATION",
        }

        validated: List[Dict[str, Any]] = []

        for item in data:
            if not isinstance(item, dict):
                continue

            file_val = item.get("file")
            line_val = item.get("line")
            bug_type_val = item.get("bug_type")
            short_reason_val = item.get("short_reason")

            if (
                isinstance(file_val, str)
                and isinstance(line_val, int)
                and bug_type_val in allowed_bug_types
                and isinstance(short_reason_val, str)
            ):
                validated.append(
                    {
                        "file": file_val,
                        "line": line_val,
                        "bug_type": bug_type_val,
                        "short_reason": short_reason_val,
                    }
                )

        return validated
