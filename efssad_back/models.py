from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
class MyUserManager(BaseUserManager):
    def create_user(self, rank, name, username, password):
        user = self.model(
            rank=rank,
            name=name,
            username=username,

        )
        user.is_mainComm = False
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, rank, name, username, password):
        user = self.create_user(
            rank=rank,
            name=name,
            username=username,
            password=password,

        )
        user.is_mainComm = True
        user.is_admin = True
        user.save(using=self._db)
        return user

class Commander(AbstractBaseUser):
    username = models.CharField(
        verbose_name='username',
        max_length=100,
        unique=True,
    )
    name = models.CharField(max_length=100)
    rank = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_mainComm = models.BooleanField(default=False)
    deploymentStatus = models.CharField(max_length=1000, default="Unassigned")

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['rank','name']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Mission(models.Model):
    missionID = models.IntegerField()
    level = models.IntegerField()
    description = models.CharField(max_length=1000)
    datetimeReceived = models.DateTimeField()
    datetimeCompleted = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=1000)
    latitude = models.FloatField()
    longitude = models.FloatField()

class AssignedCommander(models.Model):
    missionID = models.ForeignKey(Mission, on_delete=models.CASCADE)
    name = models.ForeignKey(Commander, on_delete=models.CASCADE)

class Team(models.Model):
    commander = models.ForeignKey(Commander, on_delete=models.CASCADE)
    strength = models.IntegerField()
    type = models.CharField(max_length=100)

class MessageLog(models.Model):
    missionID = models.ForeignKey(Mission, on_delete=models.CASCADE)
    dateTime = models.DateTimeField(auto_now_add = True)
    message = models.CharField(max_length=1000)
    name = models.CharField(max_length=100)
    planID = models.IntegerField()



