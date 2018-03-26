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

#redirect user to login page
#allows user to type 127.0.0.1
def user(request):
    return redirect("accounts/login")

#redirect user to their respective login menu
def mainmenu(request):
    type = request.user.username
    if Commander.objects.filter(username = type).filter(is_mainComm=True):
        return redirect("mcmain")
    elif Commander.objects.filter(username = type).filter(is_admin=False):
        return redirect("scmission")
    else:
        return redirect ("/admin")

#request main page of mc
def mcmain(request):
    context = {'all_missions' : getAllMissions(request)}
    return render(request, 'efssad_front/MCmain.html', context)

#get all missions
def getAllMissions(request):
    all_missions = Mission.objects.all()
    return all_missions

#mission detail page for mc
def missionDetail(request, missionID):
    mission = getOneMission(request, missionID)
    message = getmessagelog(request, missionID)
    context = {'mission' : mission, 'message' : message}
    return render(request, 'efssad_front/MCmission.html', context)
    # all_missions = Mission.objects.all()
    # context = {'all_missions': all_missions}
    # return render(request, 'efssad_front/MCmain.html', context)

#redirect the sc to the appropriate sc page
# def scmission(request):
#     name = request.user.name
#     Person.objects.raw('SELECT missionID FROM efssad_back WHERE name = %s', [name])
#    # missionID = userDetails.raw('SELECT missionID FROM efssad_back')
#     if missionID == -1:
#         return redirect("nomissions")
#     else:
#         return redirect("scmissionID",  missionID)
    #return render(request, 'efssad_front/SCmission.html')

#redirect the sc to the appropriate sc page
def scmission(request):
    username = request.user.name
    try:
        query = MessageLog.objects.filter(name__iexact=username)
    except MessageLog.DoesNotExist:
        return redirect("nomissions")
    if query:
        q = query.values_list('missionID', flat=True)
        return redirect("scmissionID", q.first())
    else:
        return redirect("nomissions")

#if sc has no missions
def nomissions(request):
    return render(request, 'efssad_front/SCmission.html')

#if sc has mission
def scmissionID(request, missionID):
    mission = getOneMission(request, missionID)
    message = getmessagelog(request, missionID)
    context = {'mission' : mission, 'message' : message}
    # return render(request, 'efssad_front/SCmission.html', {'mission' : mission} ,{'messages' : messages})
    return render(request, 'efssad_front/SCmission.html', context)

#get only one mission
def getOneMission(request, missionID):
    try:
        mission = Mission.objects.get(pk=missionID)
    except Mission.DoesNotExist:
        raise Http404("Mission does not exist")
    return mission

#get messagelog from database
def getmessagelog(request, missionID):
    try:
        messagelog = MessageLog.objects.filter(missionID__exact=missionID)
        # messagelog = MessageLog.objects.all()
    except MessageLog.DoesNotExist:
        raise Http404("Message log does not exist")
    return messagelog

#get archive of all past events
def archive(request):
    context = {'all_missions': getAllMissions(request)};
    return render(request, 'efssad_front/MCarchive.html', context)

#get archive details of all past events
def archiveDetail(request, missionID):
    mission = getOneMission(request, missionID)
    message = getmessagelog(request, missionID)
    context = {'mission': mission, 'message': message}
    return render(request, 'efssad_front/MCarchivedetails.html', context)

#get deployment details
def deployment(request, missionID):
    mission = getOneMission(request, missionID)
    return render(request, 'efssad_front/MCdeployment.html', {'mission' : mission})

#send message to the database
def sendmessage (request):
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

#get mission
def getMissions(request, missionDescription):
    missions = Mission.objects.get(description__contains=missionDescription)
    return missions

#
#def sendUpdate(missionid)
#def receivePlan(missionid)

#def createMission() - includes convertToObj()
#def updateMission(missionId)
#def getAllMission()
#def getOneMission(missionId)
#def getMissions(missionDescription)

#def getUnassignedCommanders(teamType)
#def assignSiteCommander(missionId, commanderId)
#def redeploy(missionId)
#def cleanup(missionId)

#def sendMessage(missionId,user)

#def convertUpdateToJSON()
#def getMessageLog(missionId)
