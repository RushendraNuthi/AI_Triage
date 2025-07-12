import json
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from ai_triage_copilot.app.models.incident_model import Incident
from ai_triage_copilot.app.models.kb_model import KnowledgeBase
from ai_triage_copilot.app import db, socketio
from ai_triage_copilot.app.services.gemini_service import get_gemini_analysis
from ai_triage_copilot.app.services.anomaly_detector import scan_for_anomalies
from ai_triage_copilot.app.services.vector_search import vector_search

incidents_bp = Blueprint('incidents', __name__)

@incidents_bp.route('/incidents/new', methods=['GET', 'POST'])
@login_required
def new_incident():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        source_system = request.form.get('source_system')
        reporter_name = current_user.username
        tags = request.form.get('tags')

        if scan_for_anomalies(description):
            flash('Anomaly detected in incident description!', 'warning')

        gemini_data = get_gemini_analysis(description)
        if gemini_data:
            try:
                analysis = json.loads(gemini_data)
                category = analysis.get('Category')
                priority = analysis.get('Priority')
                affected_entities = analysis.get('Affected Entities')
                suggested_remediation = analysis.get('Suggested Solutions')
            except json.JSONDecodeError:
                flash('Error parsing AI analysis.', 'danger')
                category = 'Uncategorized'
                priority = 'Medium'
                affected_entities = ''
                suggested_remediation = ''
        else:
            flash('Could not get AI analysis.', 'danger')
            category = 'Uncategorized'
            priority = 'Medium'
            affected_entities = ''
            suggested_remediation = ''

        new_incident = Incident(
            title=title,
            description=description,
            source_system=source_system,
            reporter_name=reporter_name,
            tags=tags,
            category=category,
            priority=priority,
            affected_entities=affected_entities,
            suggested_remediation=suggested_remediation
        )
        db.session.add(new_incident)
        db.session.commit()
        vector_search.add_to_index([description])
        socketio.emit('new_incident', new_incident.to_dict())
        flash('Incident submitted successfully!', 'success')
        return redirect(url_for('dashboard.index'))
    return render_template('submit.html')

@incidents_bp.route('/incidents/<int:incident_id>')
@login_required
def view_incident(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    kb_article = KnowledgeBase.query.filter_by(category=incident.category).first()
    return render_template('incident_view.html', incident=incident, kb_article=kb_article)
