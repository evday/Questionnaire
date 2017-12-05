import json

from django.shortcuts import render,HttpResponse,redirect

from . import models
from .forms import QuestionnaireForm

# Create your views here.
def index(request):
    questionnaire_list = models.Questionnaire.objects.all()
    return render(request,'index.html',locals())



def login(request):
    if request.method == "GET":
        return render(request,'login.html')
    elif request.is_ajax():

        state = {"state": None}
        username = request.POST.get("user")

        if username == "":
            state["state"] = "user_none"
            return HttpResponse(json.dumps(state))
        password = request.POST.get("pwd")

        if password == "":
            state["state"] = "pwd_none"
            return HttpResponse(json.dumps(state))

        user = models.UserInfo.objects.filter(username=username, password=password).first()


        if user:
            state["state"] = "login_success"
            request.session["username"] = user.username
            request.session["id"] = user.id

            print(request.session.get("id"))
        else:
            state["state"] = "failed"

        return HttpResponse(json.dumps(state))

def add(request):
    if request.method  == "GET":
        form = QuestionnaireForm()
        return render(request,'add.html',{"form":form})
    else:
        form = QuestionnaireForm(request.POST)
        if form.is_valid():

            title = form.cleaned_data.get("title")
            cls = form.cleaned_data.get("cls")
            models.Questionnaire.objects.create(title=title,cls_id=int(cls),creator_id=request.session.get("id"))
            return redirect("/index/")
        else:
            return render(request, 'add.html', {"form": form})