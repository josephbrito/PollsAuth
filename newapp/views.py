import jwt
from django.shortcuts import render, HttpResponseRedirect
from .models import User, Question, Choice
from django.utils import timezone

secret = "somewhereonlyweknowruthlesshurricanepurplesun"

def index(req):
   try:
       users = User.objects.all()

       token = jwt.decode(req.COOKIES["v"], secret, algorithms="HS256")
       if token:
           return render(req, "index.html", { "users":users, "userlogged":token, "isLogged": True, "allquestions":Question })
       else:
        return render(req, "index.html", { "users":users })
   except KeyError:
       return render(req, "index.html")

def signup(req):
    try:
        if req.COOKIES["v"]:
            return HttpResponseRedirect("/")
    except KeyError:
        return render(req, "signup.html")

def controllerSignup(req):
    try:
        hasUser = User.objects.get(username=req.POST["username"])
    except User.DoesNotExist:
        username = req.POST["username"]
        name = req.POST["name"]
        password = req.POST["password"]

        if not username or not name or not password:
            return render(req, "signup.html", { "fields_missing": True })

        user = User(username=username, name=name, password=password)
        if len(user.password) < 4:
            return render(req, "signup.html", { "password_weak": True })
        
        user.save()
        return HttpResponseRedirect("/signin")
    else:
        return render(req, "signup.html", { "error": True })
    
def signin(req):
    try:
        if req.COOKIES["v"]:
            return HttpResponseRedirect("/")
    except KeyError:
        return render(req, "signin.html")

def controllerSignin(req):
    try:
        username = req.POST["username"]
        password = req.POST["password"]
        user = User.objects.get(username=username, password=password)
        token = jwt.encode({ "username": user.username, "name":user.name }, secret, algorithm="HS256")

        response = HttpResponseRedirect("/")
        response.set_cookie("v", token, max_age=None, httponly=True)
        
        return response
    except User.DoesNotExist:
        return render(req, "signin.html", { "not_found":True })
    
def userView(req, username):
    try:
        user_token = req.COOKIES["v"]
        verify_user = jwt.decode(user_token, secret, algorithms="HS256")
        if verify_user and verify_user["username"] == username:
            user_found = User.objects.get(username=verify_user["username"], name=verify_user["name"])
            return render(req, "user.html", { "userlogged": user_found, "isLogged": True })
        else:
            return render(req, "user.html", { "error_user": True })
    except KeyError:
        return HttpResponseRedirect("/")
    except:
        return HttpResponseRedirect("/")
    
def deleting_cookie(req):
    try:
        cookie = req.COOKIES["v"]
        response = HttpResponseRedirect("/")  
        response.delete_cookie('v', cookie)  
        return response
    except KeyError:
        return HttpResponseRedirect("/")
  
def vote(req, choice_id):
    try:
        usertoken = req.COOKIES["v"]
        userdecoded = jwt.decode(usertoken, secret, algorithms="HS256")
        user = User.objects.get(username=userdecoded["username"], name=userdecoded["name"])
        if not user:
            return render(req, "index.html", { "error_vote": True })
        
        choice = Choice.objects.get(id=choice_id)
        if not user:
            return render(req, "index.html", { "error_vote": True })
        choice.votes += 1
        choice.save()
        return HttpResponseRedirect("/")
    except KeyError:
       return HttpResponseRedirect("/")
    
def newchoice(req, username):
    try:
        user = User.objects.get(username=username)

        if req.POST["choice_one"] == "" or req.POST["choice_two"] == "" or req.POST["question"] == "":
            return render(req, "user.html", { "error":True })
        
        question = user.question_set.create(question_text=req.POST["question"], pub_date=timezone.now())
        choice_one = user.choice_set.create(choice_text=req.POST["choice_one"], question_id=question.id)
        choice_two = user.choice_set.create(choice_text=req.POST["choice_two"], question_id=question.id)

        return HttpResponseRedirect("/")
    except KeyError:
        return HttpResponseRedirect("/user/jokesta")
    except:
        return render(req, "user.html", { "error":True })
