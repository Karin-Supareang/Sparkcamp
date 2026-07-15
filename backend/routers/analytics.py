from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from config.database import get_db
from database import repository
from services.analytics_service import AnalyticsService
import schemas

router = APIRouter(prefix="/quizzes", tags=["analytics"])


class _RepositoryAdapter:
    """Adapts the module-level repository functions to the (quiz_repo, analysis_repo)
    interface AnalyticsService expects, mirroring test_ai_workflow.py."""

    def __init__(self, db: Session):
        self.db = db

    def get_detailed_quiz_response_matrix(self, quiz_id: int):
        return repository.get_quiz_aggregated_data(self.db, quiz_id)

    def save_analysis_result(self, quiz_id: int, analysis_text: str):
        return repository.save_analysis_result(self.db, quiz_id, {"analysis_report": analysis_text})


@router.post("/{quiz_id}/analyze", response_model=schemas.AnalysisOut)
def analyze_quiz(quiz_id: int, db: Session = Depends(get_db)):
    if not repository.get_quiz_by_id(db, quiz_id):
        raise HTTPException(status_code=404, detail="Quiz not found")

    repo = _RepositoryAdapter(db)
    service = AnalyticsService(quiz_repo=repo, analysis_repo=repo)
    try:
        return service.run_quiz_analytics_workflow(quiz_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Analytics workflow failed: {e}")


@router.get("/{quiz_id}/analysis", response_model=schemas.SavedAnalysisOut)
def get_saved_analysis(quiz_id: int, db: Session = Depends(get_db)):
    result = repository.get_analysis_result(db, quiz_id)
    if not result:
        raise HTTPException(status_code=404, detail="No analysis found for this quiz")
    return result
