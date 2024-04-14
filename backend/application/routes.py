from application import app
from flask import request, jsonify
from .models import *

@app.route("/")
def home():
    return 'hi'

@app.route("/users", methods=["GET"])
@token_required
def get_users(current_user):
    print(current_user)
    users = User.query.all()
    results = [
        {
            "user_id": user.user_id,
            "user_name": user.user_name,
            "name": user.name,
            "email_id": user.email_id,
            "role_id": user.role_id
        } for user in users]

    return jsonify(results)

# from application.workers import celery
# from application.tasks import send_email
# @app.route("/email", methods=["POST"])
# def post_email():
#     html = request.get_json()['html']
#     email = request.get_json()['email']
#     subject = request.get_json()['subject']
#     send_email.s(eid=email, html=html, subject=subject).apply_async()
#     return jsonify({'message': 'success'})

# from application.workers import celery
# from application.tasks import unanswered_ticket_notification
# @app.route("/notification")
# def get_notif():
#     unanswered_ticket_notification.s().apply_async()
#     return "OK"