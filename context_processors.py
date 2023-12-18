from django.contrib.auth.models import User
from wwdb.models import Cast

def cast_context(request):
    return {'last': Cast.objects.last()}