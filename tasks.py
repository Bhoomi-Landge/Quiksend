# Import Celery instance from app.py
from app import celery

# Define the send_scheduled_email task
@celery.task
def send_scheduled_email(recipients, subject, body):
    # Loop through recipients and send email to each one
    for recipient in recipients:
        send_email(recipient, subject, body)
