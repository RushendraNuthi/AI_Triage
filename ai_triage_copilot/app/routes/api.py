from flask import Blueprint, jsonify, request
from ai_triage_copilot.app.models.incident_model import Incident
from ai_triage_copilot.app.services.vector_search import vector_search
from ai_triage_copilot.app.utils.feedback_handler import handle_feedback

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/incidents')
def get_incidents():
    incidents = Incident.query.all()
    return jsonify([incident.to_dict() for incident in incidents])

@api_bp.route('/api/search')
def search_incidents():
    query = request.args.get('query')
    if not query:
        return jsonify([])
    
    results = vector_search.search(query)
    return jsonify(results)

@api_bp.route('/api/feedback', methods=['POST'])
def feedback():
    data = request.get_json()
    category = data.get('category')
    feedback_type = data.get('feedback_type')
    if category and feedback_type:
        handle_feedback(category, feedback_type)
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'Invalid request'}), 400
