from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse,HttpResponseRedirect
from OTS.models import *
import random

def welcome(request):
    template=loader.get_template('welcome.html')
    return HttpResponse(template.render())
def candidateRegistrationForm(request):
    res=render(request,'registration_form.html')
    return res
def candidateRegistration(request):
    if request.method=='POST':
        username=request.POST['username']
        #Check id the user already exists
        if(len(Candidate.objects.filter(username=username))):
            userStatus=1
        else:
            candidate=Candidate()
            candidate.username=username
            candidate.password=request.POST['password']
            candidate.name=request.POST['name']
            candidate.save()
            userStatus=2
    else:
        userStatus=3 #request method is not POST
    context={
        'userStatus':userStatus
    }
    res=render(request,'registration.html',context)
    return res

def loginView(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        candidate=Candidate.objects.filter(username=username,password=password)
        if len(candidate)==0:
            loginError="Invalid Username or Password"
            res=render(request,'login.html',{'loginError':loginError})
        else:
            #login Success
            request.session['username']=candidate[0].username
            request.session['name']=candidate[0].name
            res=HttpResponseRedirect("home")
    else:
        res=render(request,'login.html')
    return res
def candidateHome(request):
    if 'name' not in request.session.keys():
        res=HttpResponseRedirect("login")
    else:
        res=render(request,'home.html')
    return res
def testPaper(request):
    if 'name' not in request.session.keys():
        res=HttpResponseRedirect("login")
    #fech question from database table
    n=int(request.GET['n'])
    question_pool=list(Question.objects.all())
    random.shuffle(question_pool)
    question_list=question_pool[:n]
    context={'questions':question_list}
    res=render(request,'test_paper.html',context)
    return res
    
def calculateTestResult(requeat):
    if 'name' not in requeat.session.keys():
        res=HttpResponseRedirect("login")
    total_attempt=0
    total_right=0
    total_wrong=0
    qid_list=[]
    for k in requeat.POST:
        if k.startswith('qno'):
            qid_list.append(int(requeat.POST[k]))
    for n in qid_list:
        question=Question.objects.get(qid=n)
        try:
            if question.ans==requeat.POST['q'+str(n)]:
                total_right+=1
            else:
                total_wrong+=1
            total_attempt+=1
        except:
            pass
    points=(total_right-total_wrong)/len(qid_list)*10
    #store result in Result table
    result=Result()
    result.username=Candidate.objects.get(username=requeat.session['username'])
    result.attempt=total_attempt
    result.right=total_right
    result.wrong=total_wrong
    result.points=points
    result.save()
    #update candidate table
    candidate=Candidate.objects.get(usrname=requeat.session['username'])
    candidate.test_attempted+=1
    candidate.points=(candidate.points*(candidate.test_attempted-1)+points)/candidate.test_attempted
    candidate.save()
    return HttpResponseRedirect('result')
def testResultHistory(request):
    pass
def showTextResult(request):
    pass
def logoutView(request):
    if 'name' in request.session.keys():
        del request.session['username']
        del request.session['name']
    return HttpResponseRedirect("login")





