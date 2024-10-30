from django.views.decorators.csrf import csrf_exempt

from myapp.slack import slack_handler


@csrf_exempt
def slack_events(request):
    return slack_handler.handle(request)
