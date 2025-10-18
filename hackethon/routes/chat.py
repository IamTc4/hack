from flask import Blueprint, render_template, request, jsonify, g
from services.firebase_service import get_firestore_db
import datetime

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/admin/chat', methods=['GET', 'POST'])
def admin_chat():
    db = get_firestore_db()
    if not db:
        return "Firestore is not available.", 500

    if request.method == 'POST':
        message_type = request.form.get('type')
        content = request.form.get('content')

        doc_ref = db.collection('live_chat').document()
        doc_ref.set({
            'type': message_type,
            'content': content,
            'timestamp': datetime.datetime.now(datetime.timezone.utc)
        })
        return redirect(url_for('chat.admin_chat'))

    return render_template('admin/chat_console.html')

@chat_bp.route('/chat/messages')
def get_chat_messages():
    db = get_firestore_db()
    if not db:
        return jsonify({"error": "Firestore is not available."}), 500

    messages_ref = db.collection('live_chat').order_by('timestamp').stream()
    messages = [doc.to_dict() for doc in messages_ref]
    return jsonify(messages)
