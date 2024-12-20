import time

from celery import shared_task


@shared_task
def send_notification_email(email, first_name, last_name):
    print("Called send activation email")
    time.sleep(60)
    raise False
    print("end task worker")


@shared_task
def export_client_data():
    print("Executer period task")
