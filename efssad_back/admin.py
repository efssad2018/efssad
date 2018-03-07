from django.contrib import admin
from .models import Mission, Commander, Team, MessageLog, Account

# Register your models here.
admin.site.register(Mission)
admin.site.register(Commander)
admin.site.register(Team)
admin.site.register(MessageLog)
admin.site.register(Account)
