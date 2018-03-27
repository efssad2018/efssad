from efssad_back.models import Commander, Mission, MessageLog, Plan
from rest_framework import serializers


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