from django.shortcuts import render, get_object_or_404, redirect
import speech_recognition as sr
from django.contrib.auth import authenticate
from django.http import HttpResponse, Http404
from django.template import loader
from efssad_back.models import Mission, AssignedCommander, MessageLog, Commander

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
    type = request.user.is_mainComm
    if type:
        return redirect("mcmain")
    elif type:
        return redirect("scmission")
    #else:
        #return redirect("login")

def mcmain(request):
    all_missions = Mission.objects.all()
    context = {'all_missions': all_missions}
    # return render(request, 'efssad_front/MCmain.html', context)
    return render(request, 'efssad_front/MCmission.html')

def scmission(request):
    return render(request, 'efssad_front/SCmission.html')

def scmissionID(request, missionID):
    try:
        mission = Mission.objects.get(pk=missionID)
    except Mission.DoesNotExist:
        raise Http404("Mission does not exist")
    return render(request, 'efssad_front/SCmission.html', {'mission' : mission})

def mission(request):
    all_missions = Mission.objects.all()
    context = {'all_missions' : all_missions}
    return render(request, 'efssad_front/MCmain.html', context)

def archive(request):
    # return render(request, 'efssad_front/MCarchive.html')
    return render(request, 'efssad_front/MCarchivedetails.html')

def deployment(request, missionID):
    try:
        mission = Mission.objects.get(pk=missionID)
    except Mission.DoesNotExist:
        raise Http404("Mission does not exist")
    return render(request, 'efssad_front/MCdeployment.html', {'mission' : mission})

def savemessage (request):
    missionid = request.POST.get('missionID')
    missionInstance = Mission.objects.get(missionID=missionid)
    message = request.POST.get('message')
    name = request.user.username
    planID = 1
    obj = MessageLog()
    obj.missionID = missionInstance
    obj.message = message
    obj.name = name
    obj.planID = planID
    obj.save()
    return redirect("scmissionID",  missionid)

def stt(request):
    return render(request, 'efssad_front/speechtotext.html')
