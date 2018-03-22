from django.shortcuts import render, get_object_or_404, redirect
import speech_recognition as sr
from django.contrib.auth import authenticate
from django.http import HttpResponse, Http404
from django.template import loader
from efssad_back.models import Mission, Account

# Create your views here.
#def login(request):

    # all_mission = Mission.objects.all()
    # template = loader.get_template('index/login.html')
    # return HttpResponse(template.render(context, request))

    # return HttpResponse('<h1>test</h1>')
    #return render(request,'registration/login.html')
    # return render(request, 'efssad_front/MCmain.html', context)
    # return render(request, 'efssad_front/MCarchive.html', context)
    # return render(request, 'efssad_front/MCmission.html', context)
    # return render(request, 'efssad_front/MCarchivedetails.html', context)
    # return render(request, 'efssad_front/SCmission.html', context)

def user(request):
    return redirect("accounts/login")

def mainmenu(request):

    if request.user.groups.filter(name='maincommander'):
        return redirect("mcmain")
    elif request.user.groups.filter(name='sitecommander'):
        return redirect("scmission")
    elif request.user.groups.filter(name='admin'):
        return redirect("/admin")

def mcmain(request):
    all_missions = Mission.objects.all()
    context = {'all_missions': all_missions}
    return render(request, 'efssad_front/MCmain.html', context)
    # return render(request, 'efssad_front/MCmission.html')

def scmission(request):
    return render(request, 'efssad_front/SCmission.html')

def mission(request):
    all_missions = Mission.objects.all()
    context = {'all_missions' : all_missions}
    return render(request, 'efssad_front/MCmain.html', context)

def archive(request):
    return render(request, 'efssad_front/MCarchive.html')

def deployment(request, missionID):
    try:
        mission = Mission.objects.get(pk=missionID)
    except Mission.DoesNotExist:
        raise Http404("Mission does not exist")
    return render(request, 'efssad_front/MCdeployment.html', {'mission' : mission})

def stt(request):
    return render(request, 'efssad_front/speechtotext.html')
