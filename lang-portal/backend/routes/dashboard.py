from fastapi import APIRouter, HTTPException
from lib.db import get_db_connection
from models import StudySession, StudyProgress, QuickStats
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/dashboard/last_study_session", response_model=StudySession, tags=["Dashboard"])
def get_last_study_session():
    """
    Retrieve information about the most recent study session.
    """
    with get_db_connection() as conn:
        query = """
        SELECT ss.id,
               sa.name AS activity_name,
               g.name AS group_name,
               ss.created_at AS start_time,
               NULL AS end_time,
               (SELECT COUNT(*) FROM word_review_items wri 
                WHERE wri.study_session_id = ss.id) as review_items_count
        FROM study_sessions ss
        LEFT JOIN study_activities sa ON sa.id = ss.study_activity_id
        LEFT JOIN groups g ON g.id = ss.group_id
        ORDER BY ss.created_at DESC
        LIMIT 1
        """
        cursor = conn.execute(query)
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(
                status_code=404, 
                detail="No study sessions found"
            )
        
        # Convert row to StudySession model
        study_session = StudySession(
            id=row[0],
            activity_name=row[1],
            group_name=row[2],
            start_time=row[3],
            end_time=row[4],
            review_items_count=row[5]
        ).model_dump()
        
        return study_session 

@router.get("/dashboard/study_progress", response_model=StudyProgress, tags=["Dashboard"])
def get_study_progress():
    """
    Retrieve overall study progress statistics.
    """
    with get_db_connection() as conn:
        # Get overall review statistics
        review_stats = conn.execute("""
            SELECT 
                COUNT(*) as total_reviews,
                SUM(CASE WHEN correct THEN 1 ELSE 0 END) as correct_reviews,
                SUM(CASE WHEN NOT correct THEN 1 ELSE 0 END) as incorrect_reviews
            FROM word_reviews
        """).fetchone()

        total_reviews = review_stats[0] or 0
        correct_reviews = review_stats[1] or 0
        incorrect_reviews = review_stats[2] or 0
        
        # Calculate accuracy rate
        accuracy_rate = (correct_reviews / total_reviews * 100) if total_reviews > 0 else 0

        # Get total study sessions
        total_sessions = conn.execute(
            "SELECT COUNT(*) FROM study_sessions"
        ).fetchone()[0]

        # Calculate total study time (using session durations)
        # For now, we'll use a fixed duration of 15 minutes per session
        total_minutes = conn.execute("""
            SELECT COUNT(*) * 15 FROM study_sessions
        """).fetchone()[0]

        # Get words reviewed by group
        words_by_group = conn.execute("""
            SELECT 
                g.id,
                g.name,
                COUNT(DISTINCT wr.word_id) as unique_words,
                COUNT(*) as total_reviews,
                SUM(CASE WHEN wr.correct THEN 1 ELSE 0 END) as correct_reviews
            FROM word_reviews wr
            JOIN study_sessions ss ON ss.id = wr.study_session_id
            JOIN groups g ON g.id = ss.group_id
            GROUP BY g.id, g.name
            ORDER BY g.name
        """).fetchall()

        words_by_group_list = [
            {
                "group_id": row[0],
                "group_name": row[1],
                "unique_words": row[2],
                "total_reviews": row[3],
                "correct_reviews": row[4],
                "accuracy_rate": (row[4] / row[3] * 100) if row[3] > 0 else 0
            }
            for row in words_by_group
        ]

        return StudyProgress(
            total_words_reviewed=total_reviews,
            total_correct=correct_reviews,
            total_incorrect=incorrect_reviews,
            accuracy_rate=accuracy_rate,
            total_study_sessions=total_sessions,
            total_study_time_minutes=total_minutes,
            words_by_group=words_by_group_list
        ).model_dump() 

@router.get("/dashboard/quick-stats", response_model=QuickStats, tags=["Dashboard"])
def get_quick_stats():
    """
    Retrieve quick overview statistics for the dashboard.
    """
    with get_db_connection() as conn:
        # Get total words count
        total_words = conn.execute(
            "SELECT COUNT(*) FROM words"
        ).fetchone()[0]

        # Get count of words with at least one correct review
        words_learned = conn.execute("""
            SELECT COUNT(DISTINCT w.id)
            FROM words w
            JOIN word_reviews wr ON wr.word_id = w.id
            WHERE wr.correct = TRUE
        """).fetchone()[0]

        # Calculate total study time (15 minutes per session for now)
        total_minutes = conn.execute("""
            SELECT COUNT(*) * 15 FROM study_sessions
        """).fetchone()[0]

        # Get accuracy rate for last 50 reviews
        recent_stats = conn.execute("""
            SELECT 
                COALESCE(
                    AVG(CASE WHEN correct THEN 100.0 ELSE 0.0 END),
                    0
                ) as accuracy
            FROM (
                SELECT correct
                FROM word_reviews
                ORDER BY created_at DESC
                LIMIT 50
            ) recent
        """).fetchone()
        recent_accuracy = recent_stats[0]

        # Calculate study streak
        today = datetime.now().date()
        streak = 0
        
        # Get last 30 days of study sessions
        study_dates = conn.execute("""
            SELECT DISTINCT date(created_at) as study_date
            FROM study_sessions
            WHERE date(created_at) <= date('now')
            ORDER BY study_date DESC
            LIMIT 30
        """).fetchall()
        
        # Convert to list of dates
        study_dates = [datetime.strptime(row[0], '%Y-%m-%d').date() for row in study_dates]
        
        if study_dates:
            current_date = study_dates[0]
            if current_date == today:
                streak = 1
                for prev_date in study_dates[1:]:
                    if current_date - prev_date == timedelta(days=1):
                        streak += 1
                        current_date = prev_date
                    else:
                        break

        return QuickStats(
            total_words=total_words,
            words_learned=words_learned,
            total_study_time_minutes=total_minutes,
            recent_accuracy=recent_accuracy,
            streak_days=streak
        ).model_dump() 