from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import lectures, quizzes, questions, responses, analytics

app = FastAPI(title="Sparkcamp Quiz API")

# No frontend URL is known yet — allow all origins during development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(lectures.router)
app.include_router(quizzes.router)
app.include_router(questions.router)
app.include_router(responses.router)
app.include_router(analytics.router)


@app.get("/health")
def health():
    return {"status": "ok"}
