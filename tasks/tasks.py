from celery import shared_task


@shared_task
def send_activation_email(email, first_name, last_name):
    pass
