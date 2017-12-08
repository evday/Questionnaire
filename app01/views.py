import json

from django.shortcuts import render,HttpResponse,redirect

from . import models
from .forms import QuestionnaireForm,QuestionModelForm,OptionModelForm

# Create your views here.
def index(request):
    questionnaire_list = models.Questionnaire.objects.all()

    for i in questionnaire_list:
        v = models.Answer.objects.filter(question__questionnaire=i).distinct().count()

        i.stu_num = v


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
        que_list = models.Question.objects.filter(questionnaire_id=pid)#获取当前问卷的所有问题
        if not que_list:#如果没有，表示该问卷还没有问题
            form = QuestionModelForm()
            yield {'form': form, 'obj': None, 'options_cls': 'hide', 'options': None}
        else:
            for que in que_list:
                form = QuestionModelForm(instance=que)
                temp = {"form":form,"obj":que,"options_cls":"hide","options":None}
                if que.ct == 2:
                    temp["options_cls"] = ""
                    #获取当前问题的所有选项
                    def inner_lop(xxx):
                        option_list = models.Option.objects.filter(question=xxx)
                        for v in option_list:
                            yield {"form":OptionModelForm(instance=v),"obj":v}
                    temp["options"] = inner_lop(que)
                yield temp




    return render(request,"edit_questionnaire.html",{"form_list":inner()})