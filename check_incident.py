from ai_triage_copilot.app import create_app, db
from ai_triage_copilot.app.models.incident_model import Incident

app = create_app()

with app.app_context():
    incident = Incident.query.filter_by(title='Test Incident').first()
    if incident:
        print('Incident created successfully!')
    else:
        print('Incident not found.')
