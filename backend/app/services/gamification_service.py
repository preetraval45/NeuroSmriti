"""
Gamification Service Layer
Stub implementation for services
"""

class BrainGamesService:
    def start_game_session(self, patient_id, game_type, difficulty):
        return {"session_id": "stub-game-123", "game_type": game_type}

    def submit_result(self, patient_id, game_session_id, score, time_seconds, mistakes):
        return {"recorded": True, "score": score}

    def get_progress(self, patient_id, days):
        return {"sessions": [], "average_score": 0.0}

    def get_leaderboard(self, game_type, timeframe):
        return {"rankings": []}


class AchievementService:
    def get_patient_achievements(self, patient_id):
        return {"achievements": [], "total_points": 0}


class ProgressTrackingService:
    def get_milestones(self, patient_id):
        return {"milestones": []}


class VRTherapyService:
    def start_session(self, patient_id, therapy_type, duration_minutes):
        return {"session_id": "stub-vr-123", "therapy_type": therapy_type}

    def end_session(self, session_id, patient_feedback):
        return {"completed": True}

    def get_session_history(self, patient_id):
        return []


# Service instances
brain_games_service = BrainGamesService()
achievement_service = AchievementService()
progress_tracking_service = ProgressTrackingService()
vr_therapy_service = VRTherapyService()
