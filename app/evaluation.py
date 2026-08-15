import os
import json

from dotenv import load_dotenv
from google import genai
from google.genai import errors
from prompts import build_evaluation_prompt
from prompts import build_interview_evaluation_prompt


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)


def evaluate_answer(question, answer):

    prompt = build_evaluation_prompt(
        question,
        answer
    )

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json"
            }
        )

    except errors.ClientError as e:

        print("Gemini API error:", e)

        return {
            "score": 0,
            "correctness": 0,
            "completeness": 0,
            "depth": 0,
            "clarity": 0,
            "relevance": 0,
            "communication": 0,
            "strengths": [],
            "weaknesses": [
                "AI evaluation was unavailable"
            ],
            "suggestions": [
                "Please try the interview again later"
            ],
            "feedback": "The AI evaluation service is temporarily unavailable."
        }

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

def validate_interview(interview):

    if not interview:
        return False

    for item in interview:

        if not isinstance(item, dict):
            return False

        if not item.get("question"):
            return False

        if not item.get("answer"):
            return False

    return True

def evaluate_interview(interview):

    if not validate_interview(interview):

        return {
            "evaluations": [],
            "overall_score": 0
        }

    prompt = build_interview_evaluation_prompt(
        interview
    )

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json"
            }
        )

    except errors.ClientError as e:

        print("Gemini API error:", e)

        return {
            "evaluations": [],
            "overall_score": 0
        }

    result = json.loads(response.text)

    evaluations = result.get(
        "evaluations",
        []
    )

    # Match each evaluation with its question
    for item in interview:

        for evaluation in evaluations:

            if (
                evaluation["question_number"]
                == item["question_number"]
            ):

                item["evaluation"] = evaluation

                break

    overall_score = calculate_overall_score(
        evaluations
    )

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

    print(
        "Overall Score:",
        result["overall_score"]
    )

    print("\nInterview Data:")

    for item in interview:

        print(item)