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


def get_all_movies(request):
    if request.method == 'POST':
        api_key = ApiKey()
        check_result = api_key.check(request)

        if check_result == type(True):
            isJson = checkJson()
            isJsonResult = isJson.isJson(request.body)

            if isJsonResult != type(True):
                return JsonResponse(isJsonResult, status=400)

            missingAttr = False
            missingAttrMsg = ""

            if 'user' not in json_data:
                missingAttr = True
                missingAttrMsg = "user is required"
            elif 'password' not in json_data:
                missingAttr = True
                missingAttrMsg = "password is required"

            if missingAttr == True:
                response_data['result'] = 'error'
                response_data['message'] = missingAttrMsg
                return JsonResponse(response_data, status=401)

            try:
                userObj = ApiUsers.objects.get(user = json_data['user'])
                password = json_data['password']
                hashedPassword = userObj.password

                check_password_result = check_password(password, hashedPassword)

                if check_password_result == False:
                    responseData['result'] = 'error'
                    responseData['message'] = 'The user does not exist or the password is incorrect'
                    return JsonResponse(responseData, status=401)

                if userObj.api_key != request.headers["user-api-key"]:
                    response_data['result'] = 'error'
                    response_data['message'] = 'Invalid Api-key'
                    return JsonResponse(response_data, status = 401)

                response_data['result'] = 'success'
                movies = Movie.objects.all()
                movie_list = []
                for movie in movies:
                    data = {}
                    data['id'] = movie.movieid
                    data['title'] = movie.movietitle
                    data['releaseDate'] = movie.releasedate
                    data['imageUrl'] = movie.imageurl
                    data['description'] = movie.description
                    movieList.append(response_movie)
                response_data['movies'] = movieList
                return JsonResponse(response_data,status=200)

            except Exception as e:
                response_data['result'] = 'error'
                response_data['message'] = 'The user does not exist or the password is incorrect'
                return JsonResponse(response_data,status=401)

        else:
            return JsonResponse(check_result, status=400)

    else:
        responseData = {}
        responseData['result'] = 'error'
        responseData['message'] = 'Invalid Request'
        return JsonResponse(responseData, status=400)
