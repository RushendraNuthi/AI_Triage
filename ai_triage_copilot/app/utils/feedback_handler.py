from ai_triage_copilot.app.models.kb_model import KnowledgeBase
from ai_triage_copilot.app import db

def handle_feedback(category, feedback_type):
    kb_article = KnowledgeBase.query.filter_by(category=category).first()
    if kb_article:
        if feedback_type == 'upvote':
            kb_article.upvotes += 1
        elif feedback_type == 'downvote':
            kb_article.downvotes += 1
        db.session.commit()
