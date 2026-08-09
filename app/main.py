from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.data.questions import QUESTIONS
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.responses import JSONResponse
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


@app.get("/")
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

@app.get("/interview/{topic}", response_class=HTMLResponse)
async def interview_page(
    request: Request,
    topic: str
):

    interview_id = str(uuid.uuid4())

    questions = QUESTIONS.get(topic.lower())

    if not questions:
        return HTMLResponse("Invalid Interview Topic")

    interviews[interview_id] = []

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
@app.post("/next-question")
async def next_question(data: dict):

    topic = data.get("topic").lower()
    current = data.get("current")
    answer = data.get("answer")
    interview_id = data.get("interview_id")

    questions = QUESTIONS.get(topic)

    if not questions:
        return JSONResponse({
            "error": "Invalid topic"
        })

    if interview_id not in interviews:
        return JSONResponse({
            "error": "Invalid interview"
        })

    interviews[interview_id].append({
        "question_number": current,
        "question": questions[current - 1],
        "answer": answer
    })

    if current >= len(questions):

        return JSONResponse({
            "finished": True,
             "interview_id": interview_id
        })

    return JSONResponse({
        "finished": False,
        "question": questions[current],
        "question_number": current + 1
    })

@app.get("/result/{interview_id}", response_class=HTMLResponse)
async def result_page(
    request: Request,
    interview_id: str
):

    answers = interviews.get(interview_id)

    if answers is None:
        return HTMLResponse("Invalid Interview ID")

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "answers": answers
        }
    )