from django.shortcuts import render
from django.http import HttpResponse
from .models import Module, Professor, Rating, moduleInstance
import json
from decimal import *

def List(request):
    # get list of modules from the database
    module_list = moduleInstance.objects.all()
    the_list = []
    for m in module_list:
        # Get list of professors
        prof_list = [];
        for p in m.professor.all():
            name = p.fname + ' ' + p.lname
            prof_list.append(name)
            
        item = {'Code': m.module.moduleCode, 'Module Name': m.module.name,
                'Year': m.year, 'Semester' : m.semester,
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

        if (length > 0):
            for rate in p.rating_set.all():
                rating += rate.rating

                rating = Decimal(rating/length).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
                rating = int(rating)
        
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

def Average(request):
    parameters = request.GET
    profID = 0;
    moduleID = 0;

    if(len(parameters) < 2):
        # TODO: add error
        print('error')

    for k,v in parameters.items():
        if(k == 'profID'):
            profID = v
        elif(k == 'moduleID'):
            moduleID = v
        else:
            # TODO: error msg
            print('error')

    # Get professor
    # TODO write error
    prof_obj = Professor.objects.get(prof_id=profID)
    prof_rating = prof_obj.rating_set.filter(moduleID__module__moduleCode = moduleID)

    # Calculating rating
    rating = 0
    length = len(prof_rating)
    if (length > 0):
        for r in prof_rating:
            rating += r.rating

            rating = Decimal(rating/length).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
            rating = int(rating)

    moduleName = Module.objects.get(moduleCode = moduleID).name
    name = prof_obj.fname + ' ' + prof_obj.lname
    payload = {'name': name, 'profID': profID, 'module': moduleName, 'moduleCode': moduleID, 'rating': rating}

    # Create HttpResponse
    http_response = HttpResponse(json.dumps(payload))
    http_response['Content-Type'] = 'application/json'
    http_response.reason_phrase = 'OK'
    return http_response
    

        
