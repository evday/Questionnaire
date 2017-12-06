import json

from django.shortcuts import render,HttpResponse,redirect

from . import models
from .forms import QuestionnaireForm,QuestionModelForm,OptionModelForm

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


def edit_questionnaire(request,pid):
    '''
      编辑问卷
      :param request:
      :param pid: 问卷id
      :return:
      '''

    def inner():

        #获取当前问卷中的所有问题
        que_list = models.Question.objects.filter(questionnaire_id=pid)
        if not que_list:
            #说明当前问卷还没有问题
            form = QuestionModelForm()
            yield {"form":form,"obj":None,"option_class":"hide","options":None}
        else:
            #含问题的问卷
            for que in que_list:
                form =  QuestionModelForm()
                temp = {"form":form,"obj":que,"option_class":"hide","options":None}
                if que.ct == 2:
                    temp["option_class"] = ''
                    #获取当前问题的所有选项
                    option_model_list = []
                    option_list = models.Option.objects.filter(question=que)
                    for v in option_list:
                        vm = OptionModelForm(instance=v)
                        option_model_list.append(vm)
                    temp["options"] = option_model_list
                yield temp
    return render(request,"edit_questionnaire.html",{"form_list":inner()})