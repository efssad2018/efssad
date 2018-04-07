from django.shortcuts import render, get_object_or_404, redirect
import speech_recognition as sr
from django.contrib.auth import authenticate
from django.http import HttpResponse, Http404
from django.template import loader
from efssad_back.models import Mission, AssignedCommander, MessageLog, Commander, Team, Plan, JsonFormat
from datetime import datetime
from itertools import chain
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from efssad_back.serializers import MissionSerializer, MessageLogSerializer, PlanSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# from drf_multiple_model.views import FlatMultipleModelAPIView
from django.contrib import messages
import json
from django.shortcuts import redirect
import requests
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse

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

#logout
def logout(request):
    request.session.flush()

    #request.session['user'] = ""
    #request.session['id'] = ""
    #request.session['dir'] = ""
    return redirect("user")

#redirect user to their respective login menu

def mainmenu(request):
    type = request.user.username
    if Commander.objects.filter(username = type).filter(is_mainComm=True):
        request.session['Sesusername'] = "mcmain"
        return redirect("mcmain")

    elif Commander.objects.filter(username = type).filter(is_admin=False):
        request.session['Sesusername'] = "scmission"
        return redirect("scmission")

    elif Commander.objects.filter(username=type).filter(is_admin=True):
        request.session['Sesusername'] = "efadmin"
        return redirect("/admin")
    else:
        request.session['Sesusername'] = None
        #del request.session['Sesusername']
        return redirect("user")

#request main page of mc
def mcmain(request):
    fav_color = request.session.get('Sesusername')
    fav_dir= request.session.get('dir')
    if fav_color is not None:
        if request.user.is_authenticated is not None:
                loginuser = request.user.username
                if Commander.objects.filter(username=loginuser).filter(is_admin=True):
                    return redirect(user)

                elif Commander.objects.filter(username=loginuser).filter(is_mainComm=False):
                    fav_id = request.session.get('Id')

                    if fav_id is not None:
                        return redirect(scmission, fav_id)
                        ###return redirect("scmission"+"/"+fav_ID)
                    else:
                        return redirect("scmission")

                elif Commander.objects.filter(username=loginuser).filter(is_mainComm=True):

                        request.session['id'] = None
                        context = {'all_missions': getAllMissions(request)}
                        request.session['dir'] = "mcmain"
                        return render(request, 'efssad_front/MCmain.html', context)
    else:
                return redirect("user")


#mission detail page for mc
def missionDetail(request, missionID):
    fav_color = request.session.get('Sesusername')
    fav_id = request.session.get('id')
    fav_dir = request.session.get('dir')

    if fav_color is not None:
        if request.user.is_authenticated is not None:
            loginuser = request.user.username
            if Commander.objects.filter(username=loginuser).filter(is_admin=True):
                return redirect("/admin")
            elif Commander.objects.filter(username=loginuser).filter(is_mainComm=False):
                if fav_dir is not None:
                    if fav_id is not None:
                        return redirect(fav_dir, fav_id)
                        ###return  redirect(fav_dir+"/"+fav_id)
                    else:
                        return redirect(fav_dir)
                else:
                    return redirect("scmission")

            else:
                mission = getOneMission(request, missionID)
                message = getmessagelog(request, missionID)
                assignedSC = getAssignedCommanders(request, missionID)

                key = 3
                dummy = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                cipher = ''

                list = []
                for x in message:

                    if x.message and x.message not in list:

                        cipher = ''
                        for c in x.message:
                            if c in dummy:
                                cipher += dummy[(dummy.index(c) + key) % len(dummy)]
                            else:
                                cipher += " "

                        dt = x.dateTime
                        cmdname = x.name
                        element = {'message': cipher, 'dateTime': dt, 'name': cmdname}

                        list.append(element)

                context = {'mission': mission, 'message': list, 'assignedSC' : assignedSC}
                request.session['dir'] = "deployment"
                request.session['id'] = missionID
                return render(request, 'efssad_front/MCmission.html', context)
    else:
        return  redirect("user")
#redirect the sc to the appropriate sc page
def scmission(request):
    fav_color = request.session.get('Sesusername')
    fav_id = request.session.get('id')
    fav_dir = request.session.get('dir')

    if fav_color is not None:
            if request.user.is_authenticated is not None:
                loginuser = request.user.username
                if Commander.objects.filter(username=loginuser).filter(is_mainComm=True):
                    if fav_dir is not None:
                        if fav_id is not None:
                            return redirect(fav_dir, fav_id)
                        else:
                            return redirect(fav_dir)
                    else:
                        return redirect("mcmain")

                elif Commander.objects.filter(username=loginuser).filter(is_admin=True):
                    return redirect("/admin")

                else:
                    username = request.user.name
                    try:
                        query = AssignedCommander.objects.filter(name=username)

                    except AssignedCommander.DoesNotExist:
                            return redirect("nomissions")

                    if query:
                        q = query.values_list('missionID', flat=True).order_by('-missionID')
                        status = getDeploymentStatus(request, username)
                        if status is not None:
                            if fav_dir is "nomissions":
                                return redirect("nomissions")
                            else:
                                request.session['dir'] = "scmissionID"
                                request.session['id'] = q.first()
                                return redirect("scmissionID", q.first())
                        else:
                            return redirect("nomissions")
                    else:
                        return redirect("nomissions")

    else:
        return redirect("user")

#if sc has no missions
def nomissions(request):
    fav_color = request.session.get('Sesusername')
    fav_id = request.session.get('id')
    fav_dir = request.session.get('dir')
    if fav_color is not None:
        if request.user.is_authenticated is not None:
            loginuser = request.user.username
            if Commander.objects.filter(username=loginuser).filter(is_admin=True):

                return redirect("/admin")
            elif Commander.objects.filter(username=loginuser).filter(is_mainComm=True):
                if fav_dir is not None:
                    if fav_id is not None:
                        return redirect(fav_dir, fav_id)
                        ###return  redirect(fav_dir+"/"+fav_id)
                    else:
                        return redirect(fav_dir)
                else:
                    return redirect("mcmain")

            else:
                if fav_id is not None:
                    return redirect("scmission")
                else:
                    request.session['dir'] = "nomissions"
                    request.session['id']= None
                    return render(request, 'efssad_front/SCmission.html')
    else:
        return redirect("user")

#if sc has mission
def scmissionID(request, missionID):

    fav_dir = request.session.get('dir')
    fav_id = request.session.get('id')
    fav_color = request.session.get('Sesusername')
    if fav_color is not None:
        # if request.method == 'POST' :
        if request.user.is_authenticated is not None:
            loginuser = request.user.username
            if Commander.objects.filter(username=loginuser).filter(is_mainComm=True):
                if fav_dir is not None:
                    if fav_id is not None:
                        return redirect(fav_dir,fav_id)

                    else:
                        return redirect(fav_dir)
                else:
                    return redirect("mcmain")

            elif Commander.objects.filter(username=loginuser).filter(is_admin=True):
                return redirect("/admin")

            elif Commander.objects.filter(username=loginuser).filter(is_admin=False):
                # Commented out the if-else to test MsgLog
                 #if fav_dir is None:
                #     will return here, dir as nomissions but sc is assigned to mission

                if fav_id is None:
                    return redirect("nomissions")
                else:
                        mission = getOneMission(request, missionID)
                        message = getmessagelog(request, missionID)

                        key = 3
                        dummy = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                        cipher = ''
                        list = []
                        emptystring = ""
                        for x in message:
                            if x.message and x.message not in list:
                                cipher = ''
                                for c in x.message:
                                    if c in dummy:
                                        cipher += dummy[(dummy.index(c) + key) % len(dummy)]
                                    else:
                                        cipher += " "
                                dt = x.dateTime
                                cmdname = x.name
                                element = {'message': cipher, 'dateTime': dt, 'name': cmdname}
                                list.append(element)

                        context = {'mission': mission, 'message': list}
                        #request.session['dir'] = "scmissionID"
                        #request.session['id'] = missionID
                        # return render(request, 'efssad_front/SCmission.html', {'mission' : mission} ,{'messages' : messages})
                        return render(request, 'efssad_front/SCmission.html', context)
    else:
        return redirect("user")


#get archive of all past events
def archive(request):
    fav_color = request.session.get('Sesusername')
    fav_ID = request.session.get('id')
    fav_dir = request.session.get('dir')


    if fav_color is not None:
        if request.user.is_authenticated is not None:
            loginuser = request.user.username
            if Commander.objects.filter(username=loginuser).filter(is_admin=True):
                    return redirect("/admin")
            elif Commander.objects.filter(username=loginuser).filter(is_mainComm=False):
                return redirect("scmission")
                if fav_dir is not None:
                    if fav_ID is not None:
                        return redirect(scmission, fav_id)
                        ###return redirect("scmission/" + fav_ID)
                    else:
                        return redirect("nomissions")
                else:
                        return redirect("scmissions")
            else:
                context = {'all_missions': getAllMissions(request)};
                request.session['dir'] = "archive"

                request.session['id'] = None
                return render(request, 'efssad_front/MCarchive.html', context)

    else:
        return redirect("user")


#get archive details of past events
def archiveDetail(request, missionID):
    fav_color = request.session.get('Sesusername')
    fav_id = request.session.get('id')
    fav_dir = request.session.get('dir')
    if fav_color is not None:
        if request.user.is_authenticated is not None:
            loginuser = request.user.username
            if Commander.objects.filter(username=loginuser).filter(is_admin=True):
                return redirect("/admin")
            elif Commander.objects.filter(username=loginuser).filter(is_mainComm=False):
                if fav_dir is not None:
                    if fav_id is not None:
                        return redirect(scmission, fav_id)
                        ###return redirect("scmission/"+fav_id)
                    else:
                        return redirect("nomissions")
                else:
                    return redirect("scmission")
            else:
                mission = getOneMissionForArchive(request, missionID)
                message = getmessagelog(request, missionID)
                assignedSC = getAssignedCommanders(request, missionID)

                key = 3
                dummy = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                cipher = ''

                list = []
                for x in message:

                    if x.message and x.message not in list:

                        cipher = ''
                        for c in x.message:
                            if c in dummy:
                                cipher += dummy[(dummy.index(c) + key) % len(dummy)]
                            else:
                                cipher += " "

                        dt = x.dateTime
                        cmdname = x.name
                        element = {'message': cipher, 'dateTime': dt, 'name': cmdname}

                        list.append(element)

                context = {'mission': mission, 'message': list, 'assignedSC' : assignedSC}
                request.session['dir'] = "archiveDetail"
                request.session['id']= missionID
                return render(request, 'efssad_front/MCarchivedetails.html', context)
    else:
        return redirect("user")
#get deployment details
def deployment(request, missionID):
    fav_color = request.session.get('Sesusername')
    fav_id = request.session.get('id')
    fav_dir = request.session.get('dir')

    if fav_color is not None:
        if request.user.is_authenticated is not None:
            loginuser = request.user.username
            if Commander.objects.filter(username=loginuser).filter(is_admin=True):
                return redirect("/admin")
            elif Commander.objects.filter(username=loginuser).filter(is_mainComm=False):
                if fav_dir is not None:
                    if fav_id is not None:
                        return redirect(fav_dir, fav_id)
                        ###return redirect(fav_dir+"/"+fav_id)
                    else:
                        return redirect(fav_dir)
                else:
                    return redirect("scmission")
            else:
                mission = getOneMission(request, missionID)
                commanders = getUnassignedCommanders(request)
                allType = ""
                for commander in commanders:
                    typelist = getTeamType(request, commander)
                    allType = list(chain(allType,typelist))
                commander = list(chain("",commanders))

                context = {'mission' : mission, 'type' : allType, 'commanders' : commander }
                request.session['id'] = missionID
                request.session['dir'] = "deployment"
                return render(request, 'efssad_front/MCdeployment.html', context)
    else:
        return redirect("user")
#get mission
def getMissions(request, missionDescription):
    missions = Mission.objects.get(description__contains=missionDescription)
    return missions

#update status - to cleanup or completed
def updateStatus(request, missionID, status):
    fav_color = request.session.get('Sesusername')
    fav_id = request.session.get('id')
    fav_dir = request.session.get('dir')

    if fav_color is not None:
        if request.user.is_authenticated is not None:
            loginuser = request.user.username
            if Commander.objects.filter(username=loginuser).filter(is_admin=True):
                return redirect("/admin")
            elif Commander.objects.filter(username=loginuser).filter(is_mainComm=False):
                if fav_dir is not None:
                    if fav_id is not None:
                        return redirect(fav_dir, fav_id)
                        ###return redirect(fav_dir+"/"+fav_id)
                    else:
                        return redirect(fav_dir)
                else:
                    return redirect("scmission")
            else:
                mission = getOneMission(request, missionID)
                mission.status = status
                mission.save()

                if mission.status.lower() == "ongoing":
                    sendSystemMessage(request, missionID, "Teams Deployed")
                    return redirect("missionDetail", missionID)

                elif mission.status.lower() == "cleanup":
                    sendSystemMessage(request, missionID, "Commence Cleanup")
                    return redirect("missionDetail", missionID)
                else:
                    mission.datetimeCompleted = datetime.now()
                    mission.save()
                    unassignSiteCommander(request, missionID)
                    sendSystemMessage(request, missionID, "Mission Completed")

                    request.session['id'] = missionID
                    request.session['dir'] = "archiveDetail"
                    return redirect(archiveDetail, missionID)
                    ###return redirect(archiveDetail+"/"+ missionID)
    else:
        return redirect("user")

#
#def sendUpdate(missionid)
#def receivePlan(missionid)

#after receiving json file, create new mission
def createMission(request): #- includes convertToObj()
    #obj = Mission()
    #obj.missionID =
    #obj.level =
    #obj.title =
    #obj.description =
    #obj.dateTimeReceived =
    #obj.datetimeCompleted =
    #obj.status =
    #obj.is_crisisAbated =
    #obj.latitude =
    #obj.longitude =
    #obj.save =
    return redirect("mcmain")
#def updateMission(missionId)

#get all missions
def getAllMissions(request):
    all_missions = Mission.objects.all()
    return all_missions

#get only one mission
def getOneMission(request, missionID):
    try:
        mission = Mission.objects.get(missionID=missionID)
    except Mission.DoesNotExist:
        raise Http404("Mission does not exist")
    return mission
#get only one mission only for Archive
def getOneMissionForArchive(request, missionID):
    try:
        mission = Mission.objects.get(missionID=missionID, status="Completed")
    except Mission.DoesNotExist:
        raise Http404("Mission does not exist")
    return mission
#def getMissions(missionDescription)


#def redeploy(missionId)
#def cleanup(missionId)

# #send message to the database
# def sendmessage(request):
#     missionid = request.POST.get('missionID')
#     missionInstance = Mission.objects.get(missionID=missionid)
#     message = request.POST.get('message')
#     name = request.user.username
#     updateID = 1
#
#     key = -3
#     dummy = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#
#     obj = MessageLog()
#     obj.missionID = (missionInstance)
#
#     cipher = ''
#     for c in message:
#         if c in dummy:
#             cipher += dummy[(dummy.index(c) + key) % len(dummy)]
#             message = cipher
#
#     obj.message = message
#     obj.name = name
#
#     obj.updateID = updateID
#     obj.save()
#     if Commander.objects.filter(username=name).filter(is_mainComm=True):
#         return redirect("missionDetail", missionid)
#     else:
#         return redirect("scmissionID", missionid)

#send message to the database
def sendmessage(request):
    fav_color = request.session.get('Sesusername')
    fav_id = request.session.get('id')
    fav_dir = request.session.get('dir')

    if fav_color is not None:
        if request.user.is_authenticated is not None:
            loginuser = request.user.username
            if Commander.objects.filter(username=loginuser).filter(is_admin=True):
                return redirect("/admin")
            elif Commander.objects.filter(username=loginuser).filter(is_mainComm=False):
                if fav_id is not None:
                    if fav_dir is not None:
                        missionid = request.POST.get('missionID')
                        missionInstance = Mission.objects.get(missionID=missionid)
                        message = request.POST.get('message')
                        name = request.user.username

                        mID = MessageLog.objects.filter(missionID=missionid).values_list('updateID', flat=True).order_by('-updateID')

                        if mID:
                            uID = mID[0]
                            updateID = uID + 1
                        else:
                            updateID = 1

                        key = -3
                        dummy = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

                        obj = MessageLog()
                        obj.missionID = (missionInstance)

                        cipher = ''
                        for c in message:
                            if c in dummy:
                                cipher += dummy[(dummy.index(c) + key) % len(dummy)]
                                message = cipher
                            else:
                                cipher += " "

                        obj.message = message
                        obj.name = name

                        obj.updateID = updateID
                        obj.save()

                       # if Commander.objects.filter(username=name).filter(is_mainComm=True):
                       #     return redirect("missionDetail", missionid)
                        # else:
                        return redirect("scmissionID", missionid)
                else:
                    return redirect("nomissions")

            else:
                if fav_id is not None:
                    missionid = request.POST.get('missionID')
                    missionInstance = Mission.objects.get(missionID=missionid)
                    message = request.POST.get('message')
                    name = request.user.username

                    mID = MessageLog.objects.filter(missionID=missionid).values_list('updateID', flat=True).order_by(
                        '-updateID')

                    if mID:
                        uID = mID[0]
                        updateID = uID + 1
                    else:
                        updateID = 1

                    key = -3
                    dummy = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

                    obj = MessageLog()
                    obj.missionID = (missionInstance)

                    cipher = ''
                    for c in message:
                        if c in dummy:
                            cipher += dummy[(dummy.index(c) + key) % len(dummy)]
                            message = cipher
                        else:
                            cipher += " "

                    obj.message = message
                    obj.name = name

                    obj.updateID = updateID
                    obj.save()
                    #if Commander.objects.filter(username=name).filter(is_mainComm=True):
                    return redirect("missionDetail", missionid)
                    #else:
                    #    return redirect("scmissionID", missionid)
                else:
                    return redirect("mcmain")
    else:
        return redirect("user")

#def convertUpdateToJSON()

#get messagelog from database
def getmessagelog(request, missionID):
    try:
        messagelog = MessageLog.objects.filter(missionID__exact=missionID)
        # messagelog = MessageLog.objects.all()
    except MessageLog.DoesNotExist:
        raise Http404("Message log does not exist")
    return messagelog

#just testing still not working
def convertToJSON(request):
    #fav_color = request.session.get('Sesusername')
    #fav_dir = request.session.get('dir')
    #fav_ID = request.session.get('ID')
    #if fav_color is not None:
    #    if request.user.is_authenticated is not None:
    #        loginuser = request.user.username
    #        if Commander.objects.filter(username=loginuser).filter(is_admin=True):
    #            return redirect("/admin")

    #        elif Commander.objects.filter(username=loginuser).filter(is_mainComm=False):
    #            if fav_dir is not None:
    #                if fav_ID is not None:
    #                    return redirect(fav_dir+"/"+fav_ID)
    #                else:
    #                    return redirect(fav_dir)
    #            else:
    #                return redirect("scmission")
    #        else :
                #if fav_dir is not None:
                #   return  redirect(fav_dir)
                #else:
                #    return redirect("mcmain")
                missionID = 1
                for m in MessageLog.objects.raw('SELECT * FROM efssad_back_messagelog WHERE missionID = %s', [missionID]):
                    print(m.updateID)
                    print(m.missionID)
                    print(m.name)
                    print(m.dateTime)
                    print(m.message)
                for c in Mission.objects.raw('SELECT * FROM efssad_back_mission WHERE missionID = %s', [missionID]):
                    print(c.is_crisisAbated)
                return render(request, 'efssad_front/testtest.html')

def searchByMissionID(request):
    fav_color = request.session.get('Sesusername')
    fav_dir = request.session.get('dir')
    fav_id = request.session.get('id')
    if fav_color is not None:
        if request.user.is_authenticated is not None:
            loginuser = request.user.username
            if Commander.objects.filter(username=loginuser).filter(is_admin=True):
                return redirect("/admin")
            elif Commander.objects.filter(username=loginuser).filter(is_mainComm=False):
                if fav_dir is not None:
                    if fav_id is not None:
                        return redirect(fav_dir, fav_id)
                       ### return redirect(fav_dir+"/"+fav_id)
                    else:
                        return  redirect(fav_dir)
                else:
                        return redirect("scmission")
            else:
                message = request.POST.get('message')
                request.session['dir'] = "archiveDetail"
                request.session['id'] = message
                return redirect("archiveDetail", message)
    else:
        return redirect("user")
#send system message when button is pressed
def sendSystemMessage(request, missionID, status):
    missionInstance = Mission.objects.get(missionID=missionID)
    message = status
    name = "System"

    mID = MessageLog.objects.filter(missionID=missionID).values_list('updateID', flat=True).order_by('-updateID')

    if mID:
        uID = mID[0]
        updateID = uID + 1
    else:
        updateID = 1

    key = -3
    dummy = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    obj = MessageLog()
    obj.missionID = (missionInstance)

    cipher = ''
    for c in message:
        if c in dummy:
            cipher += dummy[(dummy.index(c) + key) % len(dummy)]
            message = cipher
        else:
            cipher += " "

    obj.message = message
    obj.name = name

    obj.updateID = updateID
    obj.save()


# get unassigned Commanders
def getUnassignedCommanders(request):
    uaCommanders = Commander.objects.filter(is_deployed=False, is_admin=False, is_mainComm=False).values_list('name', flat=True)
    return uaCommanders

#get all teams types with available commander
def getTeamType(request, commander):
    type = Team.objects.filter(commander__iexact=commander).values_list('type', flat=True)
    return type

#get all team type
def getAllTeam(request):
    type = Team.objects.all()
    return type

# assign site commanders to mission
def assignSiteCommander(request):
    fav_color = request.session.get('Sesusername')
    fav_id = request.session.get('id')
    fav_dir = request.session.get('dir')
    if request.method == 'POST':
        if fav_color is not None:
            if request.user.is_authenticated is not None:
                loginuser = request.user.username
                if Commander.objects.filter(username=loginuser).filter(is_admin=True):
                    return redirect("/admin")
                elif Commander.objects.filter(username=loginuser).filter(is_mainComm=False):
                    if fav_dir is not None:
                        if fav_id is not None:
                            return redirect(fav_dir,fav_id)
                        else:
                            return redirect(fav_dir)
                    else:
                        return redirect("scmission")
                else:
                        missionID = request.POST.get('missionID')
                        assignSC = request.POST.get('scAva')

                        if assignSC:
                            for x in assignSC.split(','):
                                sc = Commander.objects.get(name__iexact=x)
                                # if sc:
                                sc.is_deployed = True
                                sc.save()


                            for x in assignSC.split(','):
                                assignedsc = AssignedCommander()
                                assignedsc.missionID = missionID
                                assignedsc.name = x
                                assignedsc.save()

                            updateStatus(request, missionID, "Ongoing")
                            return redirect("missionDetail", missionID)
                        else:
                            messages.info(request, 'No Available Commander!')
                            return redirect("deployment", missionID)
        else:
            return redirect("user")
    else:
        if fav_dir is not None:
            if fav_id is not None:
                return redirect(fav_dir,fav_id)
            else:
                return redirect(fav_dir)
        else:
            return redirect("mcmain")




#get assigned commanders based on missionID
def getAssignedCommanders(request, missionID):
    assignedSC = AssignedCommander.objects.filter(missionID=missionID).values_list('name', flat=True)
    assignedSC = list(chain("", assignedSC))
    return assignedSC

# assign site commanders to mission
def assignSiteCommanders(request):
    missionID = request.POST.get('missionID')
    assignSC = request.POST.get('scAva')

    if assignSC:
        for x in assignSC.split(','):
            sc = Commander.objects.get(name__iexact=x)
            # if sc:
            sc.is_deployed = True
            sc.save()


        for x in assignSC.split(','):
            assignedsc = AssignedCommander()
            assignedsc.missionID = missionID
            assignedsc.name = x
            assignedsc.save()

        updateStatus(request, missionID, "Ongoing")
        return redirect("missionDetail", missionID)
    else:
        messages.info(request, 'No Available Commander!')
        return redirect("deployment", missionID)

#unassign commanders upon mission complete
def unassignSiteCommander(request, missionID):
    assignedSC = getAssignedCommanders(request, missionID)
    for asc in assignedSC:
        ua = Commander.objects.get(name__iexact=asc)
        ua.is_deployed = False
        ua.save()

def storeJSONintoDB():
    text1 = JsonFormat.objects.values_list('json', flat=True)

    data1 = list(chain("", text1))
    str1 = ''.join(data1)
    data = json.loads(str1)

    missionObj = Mission()
    missionObj.missionID = data["crisis_id"]
    missionObj.level = data["incident_emergency_level"]
    missionObj.title = data["crisis_title"]
    missionObj.description = data["crisis_details"]
    missionObj.datetimeReceived = datetime.now()
    missionObj.latitude = data["crisis_latitude"]
    missionObj.longitude = data["crisis_longitude"]
    missionObj.save()
    planObj = Plan()
    planObj.missionID = data["crisis_id"]
    planObj.planID = data["plan_id"]
    planObj.title = data["plan_title"]
    planObj.description = data["plan_description"]
    planObj.team = data["plan_teams"]
    planObj.action = data["plan_action"]
    planObj.actiontime = datetime.now()
    planObj.save()
    return redirect("scmissionID",  missionObj.missionID)

#get deployment status of commander
def getDeploymentStatus(request, commander):
    status = list(Commander.objects.filter(name__iexact=commander).values_list('is_deployed', flat=True))
    return status

#update msglog table
def updateMsgLog(request):
    missionID = int(request.GET['missionID'])
    message = getmessagelog(request, missionID)
    key = 3
    dummy = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    cipher = ''

    list = []
    for x in message:

        if x.message and x.message not in list:

            cipher = ''
            for c in x.message:
                if c in dummy:
                    cipher += dummy[(dummy.index(c) + key) % len(dummy)]
                else:
                    cipher += " "

            dt = x.dateTime
            cmdname = x.name
            element = {'message': cipher, 'dateTime': dt, 'name': cmdname}

            list.append(element)

    return render(request, 'efssad_front/updateMsgLog.html', {'message' : list})



# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = Commander.objects.all().order_by('-name')
#     serializer_class = UserSerializer
#
#
# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer

# trying jiawei's method - dk how to return data from both mission obj and messagelogs obj into one json
# currently only returns messagelogs obj as json
def UpdatePull(request, pk):
    mission = Mission.objects.get(missionID=pk)
    messagelogs = MessageLog.objects.filter(missionID=mission.missionID)
    updates = serializers.serialize('json',messagelogs,cls=DjangoJSONEncoder)
    return HttpResponse(updates, content_type='application/json')

# using python requests library to get json from url
# dk how to maintain on the mcmain page, currently it directs to the json page
def PullFromCMO(request, pk):
    url = "http://127.0.0.1:8000/updates/new/" + pk
    print(url)
    header = {
        'Content-Type': 'application/json',
        'Authorization': 'Token 479b4e2edc4adbb44722432a8fd27e626d577b80'
    }
    r = requests.get(url, headers=header)
    jsonData = json.loads(r.content)
    # str1 = ''.join(data)
    print(jsonData)
    # w = jsonData['update']
    w = json.dumps(jsonData)
    # context = {'jsonFromCMO': json.dumps(jsonData), 'all_missions' : getAllMissions(request)}
    # return redirect('mcmain', context)
    # return HttpResponse(json.dumps(jsonData), content_type='application/json')
    context = {'jsonData' : jsonData, 'all_missions' : getAllMissions(request)}
    return render(request, 'efssad_front/MCmain.html', context)

# /updates/
class UpdateList(APIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        updates = MessageLog.objects.all()
        missions = Mission.objects.all()
        updateserializer = MessageLogSerializer(updates, many=True)
        missionserializer = MissionSerializer(missions, many=True)
        content={
            'update': updateserializer.data,
            'crisis_abated': missionserializer.data,
        }
        return Response(content)

# /updates/new/
class UpdateNew(APIView):
    def get_object(self, pk):
        try:
            mission = Mission.objects.get(missionID=pk)
            lastReceivedPlan = Plan.objects.filter(missionID=mission.missionID).order_by("-planID")[0]
            if MessageLog.objects.filter(missionID=mission.missionID):
                if lastReceivedPlan:
                    return MessageLog.objects.filter(missionID=mission.missionID).get(updateID=lastReceivedPlan.planID)
                else:
                    return MessageLog()
            else:
                return MessageLog()
        except (MessageLog.DoesNotExist, Mission.DoesNotExist):
            raise Http404

    def get(self, request):
        all_missions = getAllMissions(request)
        for m in all_missions:
            if m.level == 3:
                # testID = 1
                update = self.get_object(m.missionID)
                # update = self.get_object(pk)

                if update.missionID is not None:
                    mission = Mission.objects.get(missionID=update.missionID)
                    updateserializer = MessageLogSerializer(update)
                    missionserializer = MissionSerializer(mission)
                    content = {
                        'update': updateserializer.data,
                        'crisis_abated': missionserializer.data,
                    }
                    return Response(content)
                else:
                    raise Http404

    # def put(self, request, pk):
    #     mission = self.get_object(pk)
    #     serializer = MissionSerializer(mission, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def delete(self, request, pk):
    #     mission = self.get_object(pk)
    #     mission.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

# Lists all missions or create a new one
# missions/
class MissionList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        missions = Mission.objects.all()
        serializer = MissionSerializer(missions, many=True)
        return Response(serializer.data)

    # let them create mission object
    def post(self, request):
        serializer = MissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MissionDetail(APIView):
    def get_object(self, pk):
        try:
            return Mission.objects.get(pk=pk)
        except Mission.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        mission = self.get_object(pk)
        serializer = MissionSerializer(mission)
        return Response(serializer.data)

    def put(self, request, pk):
        mission = self.get_object(pk)
        serializer = MissionSerializer(mission, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        mission = self.get_object(pk)
        mission.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# # Lists all messagelogs or create a new one
# # messagelogs/
class MessageLogList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        messagelogs = MessageLog.objects.all()
        serializer = MessageLogSerializer(messagelogs, many=True)
        return Response(serializer.data)

    # let them create messagelogs object
    def post(self, request):
        serializer = MessageLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageLogDetail(APIView):
    def get_object(self, pk):
        try:
            return MessageLog.objects.get(pk=pk)
        except MessageLog.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        messagelog = self.get_object(pk)
        serializer = MessageLogSerializer(messagelog)
        return Response(serializer.data)

    def put(self, request, pk):
        messagelog = self.get_object(pk)
        serializer = MessageLogSerializer(messagelog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        messagelog = self.get_object(pk)
        messagelog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# # Lists all plans or create a new one
# # plans/
class PlanList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        plans = Plan.objects.all()
        serializer = PlanSerializer(plans, many=True)
        return Response(serializer.data)

    # let them create plan object
    def post(self, request):
        serializer = PlanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PlanDetail(APIView):
    def get_object(self, pk):
        try:
            return Plan.objects.get(pk=pk)
        except Plan.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        plan = self.get_object(pk)
        serializer = PlanSerializer(plan)
        return Response(serializer.data)

    def put(self, request, pk):
        plan = self.get_object(pk)
        serializer = PlanSerializer(plan, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        plan = self.get_object(pk)
        plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def testAjax(request):
    return render(request, 'efssad_front/ajax.html')
