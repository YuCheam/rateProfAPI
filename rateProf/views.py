from django.shortcuts import render
from django.http import HttpResponse
from .models import Module, Professor, Rating, moduleInstance
import json
from decimal import *
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

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

    for k,v in parameters.items():
        if(k == 'profID'):
            profID = v
        elif(k == 'moduleID'):
            moduleID = v
        else:
            http_response = HttpResponse('ERROR: Incorrect Parameter Name')
        http_response.status_code = 400
        return http_response

    # Get professor
    # TODO write error
    prof_obj = Professor.objects.get(prof_id=profID)
    prof_rating = prof_obj.rating_set.filter(module__module__moduleCode = moduleID)

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

@csrf_exempt
def Register(request):
    parameters = request.POST
    usrName = '';
    psWrd = '';
    e_mail = '';

    if len(parameters) < 3:
        # TODO: add error
        print('error')

    for k,v in parameters.items():
        if(k == 'username'):
            usrName = v
        elif(k == 'password'):
            psWrd = v
        elif(k == 'email'):
            e_mail = v
        else:
            # TODO: error msg
            print('error')

    ## Add object to db
    try:
        user = User.objects.create_user(usrName, e_mail, psWrd)
    except IntegrityError:
        http_response = HttpResponse('ERROR: Either username or email is not unique')
        http_response.status_code = 400
        return http_response
    except ValueError:
        http_response = HttpResponse('ERROR: Incorrect value username, pass, or email')
        http_response.status_code = 400
        return http_response
    
    # Create HttpResponse
    http_response = HttpResponse('User successfully created')
    http_response.status_code = 201
    return http_response

def Login(request):
    ## Get user name and pass
    parameters = request.GET
    user_name = 0;
    pass_word = 0;

    if(len(parameters) < 2):
        # TODO: add error
        print('error')

    for k,v in parameters.items():
        if(k == 'username'):
            user_name = v
        elif(k == 'password'):
            pass_word = v
        else:
            # TODO: error msg
            print('error')

    ## Authenticate and Login
    user = authenticate(username = user_name, password = pass_word)
    if user is not None:
        login(request, user)
        # backend authenticated
    else:
        http_response = HttpResponse('ERROR: invalid login')
        http_response.status_code = 400
        return http_response


    # Create HttpResponse
    http_response = HttpResponse('{} successfully logged in'.format(user.get_username()))
    http_response.status_code = 200
    return http_response

def Logout(request):
    logout(request)

    # Create HttpResponse
    http_response = HttpResponse('User successfully logged out')
    http_response.status_code = 200
    return http_response

@csrf_exempt
def Rate(request):
    parameters = request.POST
    prof_id = ''
    module_code = ''
    year = ''
    semester = 0
    rating = 0

    if len(parameters) < 3:
        # TODO: add error
        print('error')

    for k,v in parameters.items():
        if(k == 'prof_id'):
            prof_id = v
        elif(k == 'module_code'):
            module_code = v
        elif k == 'year':
            year = v
        elif k == 'semester':
            semester = v
        elif k == 'rating':
            rating = v
        else:
            # TODO: error msg
            print('error')

    ## Add object to db
    m = moduleInstance.objects.get(semester=semester, year=year,
                                   module__moduleCode=module_code,
                                   professor__prof_id=prof_id)
    p = Professor.objects.get(prof_id = prof_id)

    try:
        user = Rating.objects.create(module=m, rating=rating, profID = p)
    except IntegrityError:
        http_response = HttpResponse('ERROR: Object was not able to be created')
        http_response.status_code = 400
        return http_response


    # Create HttpResponse
    http_response = HttpResponse('Rating has been registered')
    http_response.status_code = 201
    return http_response




    

