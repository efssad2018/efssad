from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from efssad_back.models import Mission

# Create your views here.
def login(request):

    #return render(request,'index/login.html')
    all_mission = Mission.objects.all()
    template = loader.get_template('index/login.html')
    context = {

    }
    # return HttpResponse('<h1>test</h1>')