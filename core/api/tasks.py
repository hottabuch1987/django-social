from celery import shared_task
from account.models import User


@shared_task
def get_user_queryset_async(slug):
    queryset = User.objects.filter(slug=slug)
    return list(queryset.values())

