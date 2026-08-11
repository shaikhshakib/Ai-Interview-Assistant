def build_evaluation_prompt(question, answer):

    prompt = f"""
You are an AI technical interviewer.

Evaluate the candidate's answer to the interview question below.

Interview Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer based on:

1. Correctness
2. Completeness
3. Depth of understanding
4. Clarity
5. Relevance
6. Professional communication

Give each category a score from 0 to 10.

Also provide:

- Overall score from 0 to 10
- Strengths
- Weaknesses
- Specific suggestions for improvement
- Detailed feedback

Do not judge the candidate based only on answer length.
A short answer can receive a high score if it is accurate,
complete for the question, and demonstrates understanding.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "score": 0,
    "correctness": 0,
    "completeness": 0,
    "depth": 0,
    "clarity": 0,
    "relevance": 0,
    "communication": 0,
    "strengths": [],
    "weaknesses": [],
    "suggestions": [],
    "feedback": ""
}}

All scores must be numbers from 0 to 10.

Do not include Markdown.
Do not include ```json.
Do not include any text outside the JSON object.
"""

    return prompt