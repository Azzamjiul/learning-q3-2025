import time

from app.celery_app import celery_app


@celery_app.task
def send_email(to: str, subject: str, body: str):
    time.sleep(3)  # Simulate delay
    print(f"Sending email to {to} with subject '{subject}' and body '{body}'")
