from ai_triage_copilot.app import db

class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    source_system = db.Column(db.String(255), nullable=False, default='Manual')
    reporter_name = db.Column(db.String(255), nullable=True)
    tags = db.Column(db.String(255), nullable=True)
    category = db.Column(db.String(100), nullable=True)
    priority = db.Column(db.String(50), nullable=True)
    affected_entities = db.Column(db.String(255), nullable=True)
    suggested_remediation = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='New')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<Incident {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'source_system': self.source_system,
            'reporter_name': self.reporter_name,
            'tags': self.tags,
            'category': self.category,
            'priority': self.priority,
            'affected_entities': self.affected_entities,
            'suggested_remediation': self.suggested_remediation,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
