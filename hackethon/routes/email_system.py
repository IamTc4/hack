from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.email import EmailDraft

email_bp = Blueprint('email', __name__)

@email_bp.route('/admin/emails')
def list_emails():
    drafts = EmailDraft.query.all()
    return render_template('admin/emails.html', drafts=drafts)

@email_bp.route('/admin/emails/create', methods=['GET', 'POST'])
def create_email():
    if request.method == 'POST':
        subject = request.form.get('subject')
        body = request.form.get('body')
        recipient_group = request.form.get('recipient_group')

        new_draft = EmailDraft(subject=subject, body=body, recipient_group=recipient_group)
        db.session.add(new_draft)
        db.session.commit()

        flash('Draft saved successfully!')
        return redirect(url_for('email.list_emails'))

    return render_template('admin/email_form.html')

@email_bp.route('/admin/emails/edit/<int:draft_id>', methods=['GET', 'POST'])
def edit_email(draft_id):
    draft = EmailDraft.query.get_or_404(draft_id)
    if request.method == 'POST':
        draft.subject = request.form.get('subject')
        draft.body = request.form.get('body')
        draft.recipient_group = request.form.get('recipient_group')
        db.session.commit()

        flash('Draft updated successfully!')
        return redirect(url_for('email.list_emails'))

    return render_template('admin/email_form.html', draft=draft)

@email_bp.route('/admin/emails/delete/<int:draft_id>', methods=['POST'])
def delete_email(draft_id):
    draft = EmailDraft.query.get_or_404(draft_id)
    db.session.delete(draft)
    db.session.commit()

    flash('Draft deleted successfully!')
    return redirect(url_for('email.list_emails'))

@email_bp.route('/admin/emails/send/<int:draft_id>', methods=['POST'])
def send_email(draft_id):
    draft = EmailDraft.query.get_or_404(draft_id)

    # Mock sending the email
    print(f"Sending email to {draft.recipient_group}:")
    print(f"Subject: {draft.subject}")
    print(f"Body: {draft.body}")

    flash('Email sent successfully!')
    return redirect(url_for('email.list_emails'))
