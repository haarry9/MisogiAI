from app.celery_worker.celery import celery
import time

@celery.task
def send_order_confirmation_email(order_id: int, email: str):
    # Simulate sending email
    time.sleep(2)
    return {"order_id": order_id, "email": email, "status": "sent"}