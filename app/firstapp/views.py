# Create your views here.
#IMPORT models
from .models import Movie,ApiUsers

#IMPORT LIBRARIRES/FUNCTIONS
#from django.shortcuts import render , HttpResponse
from django.http import JsonResponse, HttpResponse
import json
from firstapp.customClasses import *
#IMPORT DJANGO PASSWORD HASH GENERATOR AND COMPARE
from django.contrib.auth.hashers import make_password, check_password

#check_password(noHashPassword,HashedPassword) this funcion validate if the password match to the hash

def login(request):

    #VALIDATE METHOD
    if request.method == 'POST':

        #DECLARE RESPONSE
        responseData = {}

        #CHECK JSON STRUCTURE
        isJson = checkJson()
        isJsonResult = isJson.isJson(request.body)

        if (type(isJsonResult) == type(True)):
            jsonBody = json.loads(request.body)

            #CHECK JSON CONTENT
            if 'user' not in jsonBody:
                responseData['result'] = 'error'
                responseData['message'] = 'user is required'
                return JsonResponse(responseData, status=401)

            if 'password' not in jsonBody:
                responseData['result'] = 'error'
                responseData['message'] = 'password is required'
                return JsonResponse(responseData, status=401)

            #CHECK IF USER EXITST
            if len(ApiUsers.objects.get(user=jsonBody['user'])) > 1:
                #TAKE PASSWORD OF THE USER
                user = ApiUsers.objects.get(user=jsonBody['user'], password=jsonBody['password'])

                #CHECK IF PASSWORD IS CORRECT
                if check_password(jsonBody['password'], user.password):
                    #CHECK IF USER HAS API-KEY
                    if user.api_key == None:
                        api_key = ApiKey()
                        user.api_key = api_key.generate_key_complex()
                        user.save()

                    #RETURN RESPONSE
                    responseData['result'] = 'success'
                    responseData['message'] = 'Valid Credentials'
                    responseData['userApiKey'] = user.api_key
                    return JsonResponse(responseData, status=200)

                else:
                    responseData['result'] = 'error'
                    responseData['message'] = 'The user does not exist or the password is incorrect'
                    return JsonResponse(responseData, status=401)

            else:
                responseData['result'] = 'error'
                responseData['message'] = 'The user does not exist or the password is incorrect'
                return JsonResponse(responseData, status=401)

        else:
            return isJsonResult

    else:
        responseData = {}
        responseData['result'] = 'error'
        responseData['message'] = 'Invalid Request'
        return JsonResponse(responseData, status=400)


def makepassword(request,password):
    hashPassword = make_password(password)
    response_data = {}
    response_data['password'] = hashPassword
    return JsonResponse(response_data, status=200)
