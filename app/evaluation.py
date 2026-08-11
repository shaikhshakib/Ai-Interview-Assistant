import os
import json

from dotenv import load_dotenv
from google import genai

from prompts import build_evaluation_prompt


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)


def evaluate_answer(question, answer):

    prompt = build_evaluation_prompt(
        question,
        answer
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    evaluation = json.loads(response.text)

    return evaluation


if __name__ == "__main__":

    result = evaluate_answer(
        "What is Python?",
        "Python is a high-level programming language."
    )

    print(result)

    print("\nScore:", result["score"])
    print("Depth:", result["depth"])
    print("Feedback:", result["feedback"])