import os
import json

from dotenv import load_dotenv
from google import genai

from app.prompts import build_evaluation_prompt


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


def calculate_overall_score(evaluations):

    if not evaluations:
        return 0

    total_score = sum(
        evaluation["score"]
        for evaluation in evaluations
    )

    overall_score = total_score / len(evaluations)

    return round(overall_score, 2)


def evaluate_interview(interview):

    evaluations = []

    for item in interview:

        evaluation = evaluate_answer(
            item["question"],
            item["answer"]
        )

        item["evaluation"] = evaluation

        evaluations.append(evaluation)

    overall_score = calculate_overall_score(evaluations)

    return {
        "evaluations": evaluations,
        "overall_score": overall_score
    }


if __name__ == "__main__":

    interview = [
        {
            "question_number": 1,
            "question": "What is Python?",
            "answer": "Python is a high-level programming language."
        },
        {
            "question_number": 2,
            "question": "What is a list?",
            "answer": "A list is a collection of items."
        }
    ]

    result = evaluate_interview(interview)

    print("Overall Score:", result["overall_score"])

    print("\nInterview Data:")

    for item in interview:
        print(item)