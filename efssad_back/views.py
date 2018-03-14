from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from efssad_back.models import Mission, Account

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

def mcmain(request):
    # return render(request, 'efssad_front/MCmain.html')
    return render(request, 'efssad_front/MCmission.html')

def scmission(request):
    return render(request, 'efssad_front/SCmission.html')

def mission(request):
    return render(request, 'efssad_front/MCmain.html')

def archive(request):
    return render(request, 'efssad_front/MCarchive.html')

