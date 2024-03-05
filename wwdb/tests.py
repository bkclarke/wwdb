from django.db.models import Count, Q
from django.db.models import Avg, Count, Min, Sum, Max
from .models import Cast



class Winches:
    def __init__(self, winch):
        self.winch=winch 

startdate="2023-7-1 14:18:00"
enddate="2024-2-2 15:40:00"
casts=Cast.objects.filter(startdate__range=[startdate, enddate])
winches=Cast.objects.filter(startdate__range=[startdate, enddate]).values('winch').distinct()

instancenames=['winch1','winch2','winch3']

holder={name:Winches(name=name) for name in instancenames}

holder['winch1'].name
