import os
import time

from google import genai
from google.genai.errors import ClientError

from diff_parser import ScenarioChange

_MODEL = "gemini-2.5-flash-lite"
_RETRY_DELAY = 15


def is_doc_relevant(change: ScenarioChange, retries: int = 2) -> bool:
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    prompt = (
        "You are reviewing a Python file added to krkn-chaos, a chaos engineering framework.\n"
        "Determine if this file defines a user-facing chaos scenario that should be documented.\n"
        "Reply with only YES or NO.\n\n"
        f"File: {change.file_path}\n"
        f"Classes: {', '.join(change.classes) or 'none'}\n"
        f"Functions: {', '.join(change.functions[:5]) or 'none'}\n\n"
        f"Source (first 2000 chars):\n{change.source[:2000]}"
    )

    for attempt in range(retries + 1):
        try:
            response = client.models.generate_content(model=_MODEL, contents=prompt)
            return response.text.strip().upper().startswith("YES")
        except ClientError as e:
            if e.status_code == 429 and attempt < retries:
                time.sleep(_RETRY_DELAY)
                continue
            raise
