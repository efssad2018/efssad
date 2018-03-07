from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
# from efssad_back.models import Mission

# Create your views here.
def login(request):

    # all_mission = Mission.objects.all()
    # template = loader.get_template('index/login.html')
    context = {"message" : "Hello"}
    # return HttpResponse(template.render(context, request))

    # return HttpResponse('<h1>test</h1>')
    return render(request,'efssad_front/login.html', context)