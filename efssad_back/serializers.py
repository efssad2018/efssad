# from django.contrib.auth.models import User, Group
from efssad_back.models import Commander, Mission, MessageLog, Plan
from rest_framework import serializers


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Commander
#         fields = ('username', 'name', 'rank', 'is_active', 'is_admin', 'is_mainComm', 'is_deployed')
#
#
# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ('url', 'name')

class MissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = ('id', 'missionID', 'level', 'title', 'description', 'datetimeReceived', 'is_crisisAbated', 'latitude', 'longitude')

class MessageLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageLog
        fields = ('id', 'updateID', 'missionID', 'name', 'dateTime', 'message')

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ('id', 'planID', 'title', 'team', 'description', 'action', 'actiontime')