from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ai_triage_copilot.app.models.kb_model import KnowledgeBase
from ai_triage_copilot.app import db

playbooks_bp = Blueprint('playbooks', __name__)

@playbooks_bp.route('/playbooks')
@login_required
def list_playbooks():
    playbooks = KnowledgeBase.query.all()
    return render_template('playbooks.html', playbooks=playbooks)

@playbooks_bp.route('/playbooks/edit/<category>', methods=['GET', 'POST'])
@login_required
def edit_playbook(category):
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('dashboard.index'))
        
    playbook = KnowledgeBase.query.filter_by(category=category).first_or_404()
    if request.method == 'POST':
        playbook.content = request.form['content']
        db.session.commit()
        flash('Playbook updated successfully!', 'success')
        return redirect(url_for('playbooks.list_playbooks'))
    return render_template('edit_playbook.html', playbook=playbook)
