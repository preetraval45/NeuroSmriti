"""
Social Support Service Layer
Stub implementation for services
"""

class SupportGroupService:
    def search_groups(self, location, radius_km, group_type):
        return []

    def get_online_groups(self):
        return []


class ForumService:
    def create_post(self, user_id, category, title, content, is_anonymous):
        return {"post_id": "stub-123", "created": True}

    def create_reply(self, user_id, post_id, content, is_anonymous):
        return {"reply_id": "stub-456", "created": True}

    def get_posts(self, category, limit, offset):
        return []


class EducationService:
    def search_resources(self, topic, content_type, difficulty_level):
        return []

    def get_personalized_recommendations(self, patient_id):
        return []


class ExpertQAService:
    def submit_question(self, user_id, patient_id, question, category, is_urgent):
        return {"question_id": "stub-789", "submitted": True}

    def get_user_answers(self, user_id):
        return []


class PeerMatchingService:
    def find_matches(self, caregiver_id, patient_diagnosis_stage, caregiver_role, preferred_language):
        return []


# Service instances
support_group_service = SupportGroupService()
forum_service = ForumService()
education_service = EducationService()
expert_qa_service = ExpertQAService()
peer_matching_service = PeerMatchingService()
