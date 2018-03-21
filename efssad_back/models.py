from django.db import models

# Create your models here.
class Mission(models.Model):
    missionID = models.IntegerField()
    level = models.IntegerField()
    description = models.CharField(max_length=1000)
    datetimeReceived = models.DateTimeField()
    datetimeCompleted = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=1000)
    latitude = models.FloatField()
    longitude = models.FloatField()

class Commander(models.Model):
    missionID = models.ForeignKey(Mission, on_delete=models.CASCADE)
    rank = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    deploymentStatus = models.CharField(max_length=1000)

class Team(models.Model):
    commander = models.ForeignKey(Commander, on_delete=models.CASCADE)
    strength = models.IntegerField()
    type = models.CharField(max_length=100)

class MessageLog(models.Model):
    missionID = models.ForeignKey(Mission, on_delete=models.CASCADE)
    dateTime = models.DateTimeField()
    message = models.CharField(max_length=1000)
    name = models.CharField(max_length=100)
    planID = models.CharField(max_length=100)

class Account(models.Model):
    commanderID = models.ForeignKey(Commander, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)



