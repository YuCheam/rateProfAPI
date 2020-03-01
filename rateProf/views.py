from django.shortcuts import render
from django.http import HttpResponse
from .models import Module, Professor, Rating
import json

def List(request):
    #get list of modules from the database
    module_list = Module.objects.all()
    the_list = []
    for module in module_list:
        # Get list of professors
        prof_list = [];
        for p in module.professor.all():
            name = p.fname + ' ' + p.lname
            prof_list.append(name)
        item = {'Code': module.moduleCode, 'Module Name': module.name,
                'Year': module.year, 'Semester' : module.semester,
                'Taught By' : prof_list}
        the_list.append(item)

    # Create Payload
    payload = {'module_list' : the_list}

    # Create HttpResponse
    http_response = HttpResponse(json.dumps(payload))
    http_response['Content-Type'] = 'application/json'
    http_response.reason_phrase = 'OK'
    return http_response

def View(request):
    retList = []

    # Get list of professors
    prof_list = Professor.objects.all()
    for p in prof_list:
        rating = 0 
        length = len(p.rating_set.all())

        for rate in p.rating_set.all():
            rating += rate.rating

        rating = round(rating/length)
        name = p.fname + ' ' + p.lname
        item = {'Name' : name, 'Rating' : rating}
        retList.append(item)

    # Create payload
    payload = {'professors' : retList}

    # Create HttpResponse
    http_response = HttpResponse(json.dumps(payload))
    http_response['Content-Type'] = 'application/json'
    http_response.reason_phrase = 'OK'
    return http_response


        
