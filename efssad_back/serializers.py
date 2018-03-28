from efssad_back.models import Commander, Mission, MessageLog, Plan
from rest_framework import serializers
from rest_framework.fields import Field


class MissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        # fields = ('id', 'missionID', 'level', 'title', 'description', 'datetimeReceived', 'is_crisisAbated', 'latitude', 'longitude')
        fields = ('missionID', 'is_crisisAbated')

class MessageLogSerializer(serializers.ModelSerializer):
    # mission = MissionSerializer(read_only=True)
    class Meta:
        model = MessageLog
        fields = ('updateID', 'missionID', 'name', 'dateTime', 'message')

# class MessageLogSerializer(serializers.Serializer):
#     update_id = Field(source='updateID')
#     update_mission_id = Field(source='missionID')
#     update_commander = Field(source='name')
#     update_date_time = Field(source='dateTime')
#     update_message = Field(source='message')
#     crisis_abated = Field(source='Mission.is_crisisAbated')

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ('id', 'planID', 'title', 'team', 'description', 'action', 'actiontime')