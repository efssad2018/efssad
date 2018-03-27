from django.shortcuts import render, get_object_or_404, redirect
import speech_recognition as sr
from django.contrib.auth import authenticate
from django.http import HttpResponse, Http404
from django.template import loader
from efssad_back.models import Mission, AssignedCommander, MessageLog, Commander, Plan
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from efssad_back.serializers import MissionSerializer, MessageLogSerializer, PlanSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

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

#mission detail page for mc
def missionDetail(request, missionID):
    mission = getOneMission(request, missionID)
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

    context = {'mission': mission, 'message': list}
    # return render(request, 'efssad_front/SCmission.html', {'mission' : mission} ,{'messages' : messages})
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
        query = AssignedCommander.objects.filter(name__iexact=username)
    except AssignedCommander.DoesNotExist:
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


    key = 3
    dummy = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    cipher = ''

    list = []
    emptystring =""
    for x in message:

        if x.message and x.message not in list:

            cipher = ''

            for c in x.message:

                if c in dummy:
                        cipher += dummy[(dummy.index(c) + key) % len(dummy)]
                else:
                    cipher += " "

            dt = x.dateTime
            cmdname= x.name
            element ={'message': cipher,'dateTime': dt,'name': cmdname}

            list.append(element)

    context = {'mission' : mission, 'message' : list}
    # return render(request, 'efssad_front/SCmission.html', {'mission' : mission} ,{'messages' : messages})
    return render(request, 'efssad_front/SCmission.html', context)


#get archive of all past events
def archive(request):
    context = {'all_missions': getAllMissions(request)};
    return render(request, 'efssad_front/MCarchive.html', context)

#get archive details of past events
def archiveDetail(request, missionID):
    mission = getOneMission(request, missionID)
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

    context = {'mission': mission, 'message': list}
    # return render(request, 'efssad_front/SCmission.html', {'mission' : mission} ,{'messages' : messages})
    return render(request, 'efssad_front/MCarchivedetails.html', context)

#get deployment details
def deployment(request, missionID):
    mission = getOneMission(request, missionID)
    return render(request, 'efssad_front/MCdeployment.html', {'mission' : mission})

#get mission
def getMissions(request, missionDescription):
    missions = Mission.objects.get(description__contains=missionDescription)
    return missions

#update status - to cleanup or completed
def updateStatus(request, missionID, status):
    mission = getOneMission(request, missionID)
    mission.status = status
    mission.save()

    if mission.status.lower() == "cleanup":
        sendSystemMessage(request, missionID, "Commence Cleanup")
        return redirect("missionDetail", missionID)
    else:
        mission.datetimeCompleted = datetime.now()
        mission.save()
        sendSystemMessage(request, missionID, "Mission Completed")
        return redirect("archiveDetail", missionID)


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
        mission = Mission.objects.get(pk=missionID)
    except Mission.DoesNotExist:
        raise Http404("Mission does not exist")
    return mission
#def getMissions(missionDescription)

#def assignSiteCommander(missionId, commanderId)
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
    if Commander.objects.filter(username=name).filter(is_mainComm=True):
        return redirect("missionDetail", missionid)
    else:
        return redirect("scmissionID", missionid)


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
    message = request.POST.get('message')
    return redirect("archiveDetail", message)

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
# def getUnassignedCommanders(request):

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