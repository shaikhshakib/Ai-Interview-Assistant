from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.data.questions import QUESTIONS
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.responses import JSONResponse


app = FastAPI(title="AI Interview Assistant")

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

    questions = QUESTIONS.get(topic.lower())

    if not questions:
        return HTMLResponse("Invalid Interview Topic")

    return templates.TemplateResponse(
        request=request,
        name="interview.html",
        context={
            "topic": topic.capitalize(),
            "question": questions[0],
            "question_number": 1,
            "total_questions": len(questions)
        }
    )
@app.post("/next-question")
async def next_question(data: dict):

    topic = data.get("topic").lower()

    current = data.get("current")

    questions = QUESTIONS.get(topic)

    if current >= len(questions):

        return JSONResponse({
            "finished": True
        })

    return JSONResponse({

        "finished": False,

        "question": questions[current],

        "question_number": current + 1

    })