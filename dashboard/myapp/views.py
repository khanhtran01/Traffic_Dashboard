from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from .models import Humis, Temp, BadCar
from .forms import ResgisterForm
from django.views import View
import serial.tools.list_ports
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
# @login_required(login_url='myapp:login')
def index(request):
    return render(request, "myapp/userBoard.html")

@login_required(login_url='myapp:login')
def pushHumi(request):
    if request.method == "POST":
        humiInput = Humis(humi = int(request.POST['humi']), time= datetime.datetime.now()) 
        humiInput.save()
        return JsonResponse({'data': "here is new data", 'message' : "input complete"}, status=200)
    else:
        return JsonResponse({'data': "here is new data", 'message' : "failed"}, status=200)
    
# @login_required(login_url='myapp:login')
# def detailsView(request, idx):
#     q = Question.objects.get(pk=idx)
#     res = {
#         'details': q
#     }
#     return render(request, "myapp/detail.html", res)


@login_required(login_url='myapp:login')
def dashBoardView(request):
    return render(request, "myapp/dashboard.html")


# @login_required(login_url='myapp:login')
def initHumi(request):
    humis = Humis.objects.all().order_by('-id')[:20:-1]
    temps = Temp.objects.all().order_by('-id')[:20:-1]
    badcars = BadCar.objects.all().order_by('-id')[:20:-1]
    humilist = []
    humitime = []
    templist = []
    temptime = []
    badcarlist = []
    badcartime = []
    for humi in humis:
        humilist += [humi.humi]
        humitime += [humi.time]
    for temp in temps:
        templist += [temp.temp]
        temptime += [temp.time]
    for car in badcars:
        badcarlist += [car.badcar]
        badcartime += [car.time]
    
    resu = {
        'humidata' : humilist,
        'humitime' : humitime,
        'tempdata' : templist,
        'temptime' : temptime,
        'cardata' : badcarlist,
        'cartime' : badcartime
    }
    return JsonResponse(resu, status= 200)


@login_required(login_url='myapp:login')
def getNewestData(request):
    q = Humis.objects.all().order_by('-id')[:1]
    resu = {
        'data' : q[0].humi,
        'time' : q[0].time
    }
    return JsonResponse(resu, status= 200)
class LoginClass(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('myapp:dashboard')
        return render(request, "myapp/login.htm")
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        my_user = authenticate(request ,username = username, password = password)
        
        if my_user is not None:
            login(request, my_user)
            return redirect('myapp:dashboard')
        else:
            messages.info(request, 'Tên người dùng hoặc mật khẩu không đúng')
        
        return render(request, 'myapp/login.htm')
class RegisterClass(View):
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('myapp:index')
        form = ResgisterForm()
        context = {'forms': form}
        return render(request, "myapp/register.htm", context)
    
    def post(self,request):
        form = ResgisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('myapp:login')
        context = {'forms': form}
        return render(request, "myapp/register.htm", context)
    
    
def logoutUser(request):
    logout(request)
    return redirect('myapp:login')

@login_required(login_url='myapp:login')
def pushData(request):
    if request.method == "POST":
        humi_value = request.POST['humi']
        temp_value = request.POST['temp']
        humiInput = Humis(humi = int(humi_value), time= datetime.datetime.now())
        tempInput = Temp(temp = int(temp_value), time= datetime.datetime.now())
        humiInput.save()
        tempInput.save()
        return JsonResponse({'data': "here is new data", 'message' : "input complete"}, status=200)
    else:
        return JsonResponse({'data': "here is new data", 'message' : "failed"}, status=200)