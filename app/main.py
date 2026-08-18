from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from google.genai import errors
from app.data.questions import QUESTIONS
from app.evaluation import evaluate_interview

from fastapi.responses import HTMLResponse, JSONResponse

import uuid


app = FastAPI(title="AI Interview Assistant")


interviews = {}


app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)


templates = Jinja2Templates(
    directory="app/templates"
)


# -----------------------------------
# HOME PAGE
# -----------------------------------

@app.get("/")
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# -----------------------------------
# START INTERVIEW
# -----------------------------------

@app.get(
    "/interview/{topic}",
    response_class=HTMLResponse
)
async def interview_page(
    request: Request,
    topic: str
):

    interview_id = str(uuid.uuid4())

    questions = QUESTIONS.get(
        topic.lower()
    )

    if not questions:

        return HTMLResponse(
            "Invalid Interview Topic"
        )

    interviews[interview_id] = {
    "answers": [],
    "status": "in_progress"
}

    return templates.TemplateResponse(
        request=request,
        name="interview.html",
        context={
            "topic": topic.capitalize(),
            "question": questions[0],
            "question_number": 1,
            "total_questions": len(questions),
            "interview_id": interview_id
        }
    )


# -----------------------------------
# NEXT QUESTION
# -----------------------------------

@app.post("/next-question")
async def next_question(data: dict):

    topic = data.get("topic").lower()

    current = data.get("current")

    answer = data.get("answer")

    interview_id = data.get("interview_id")


    questions = QUESTIONS.get(topic)


    # Check topic

    if not questions:

        return JSONResponse({
            "error": "Invalid topic"
        })


    # Check interview ID

    if interview_id not in interviews:

        return JSONResponse({
            "error": "Invalid interview"
        })


    # Store answer

    interviews[interview_id]["answers"].append({

        "question_number": current,

        "question": questions[current - 1],

        "answer": answer

    })


    # Check if interview is finished

    if current >= len(questions):

        result = evaluate_interview(
        interviews[interview_id]["answers"]
    )

    interviews[interview_id]["evaluations"] = result["evaluations"]
    interviews[interview_id]["overall_score"] = result["overall_score"]

    interviews[interview_id]["status"] = "completed"

    return JSONResponse({
        "finished": True,
        "interview_id": interview_id
    })


    # Return next question

    return JSONResponse({

        "finished": False,

        "question": questions[current],

        "question_number": current + 1

    })


# -----------------------------------
# RESULT PAGE
# -----------------------------------

@app.get(
    "/result/{interview_id}",
    response_class=HTMLResponse
)
async def result_page(
    request: Request,
    interview_id: str
):

    interview = interviews.get(
        interview_id
    )


    # Check interview ID

    if not interview:

        return HTMLResponse(
            "Invalid interview"
        )


    return templates.TemplateResponse(

        request=request,

        name="result.html",

        context={

            "answers": interview["answers"],

            "overall_score": interview.get(
                "overall_score",
                0
            )

        }

    )