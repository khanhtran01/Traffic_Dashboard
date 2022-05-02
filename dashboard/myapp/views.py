from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from .models import Humis, Temp, BadCar
from .forms import ResgisterForm
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models.functions import ExtractWeek, ExtractYear, ExtractMonth
from django.db.models import Avg
from django.contrib import messages
from Adafruit_IO import Client
import datetime

# @login_required(login_url='myapp:login')
def pushControl(data):
    aio = Client('khanhtran01', 'aio_OpaI071fRZr3S64zA2MUmiPPZGmx')
    feed = aio.feeds('control')
    res = ''
    if data == 'emer':
        res = '{"emer":"1","slow":"0"}'
    else: res = '{"emer":"0","slow":"1"}'
    aio.send_data(feed.key, res)
    

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
    if request.method == "POST":
        pushControl(request.POST['Setlight'])
        return render(request, "myapp/dashboard.html")
        
    
    return render(request, "myapp/dashboard.html")

def initDataWeek(request):
    Humidata = (Humis.objects
                .annotate(week = ExtractWeek('time'))
                .values('week')
                .annotate(avg_humi=Avg('humi')))
    Tempdata = (Temp.objects
                .annotate(week = ExtractWeek('time'))
                .values('week')
                .annotate(avg_temp=Avg('temp')))
    HumidataMonth = (Humis.objects
                .annotate(month = ExtractMonth('time'))
                .values('month')
                .annotate(avg_humi=Avg('humi')))
    TempdataMonth = (Temp.objects
                .annotate(month = ExtractMonth('time'))
                .values('month')
                .annotate(avg_temp=Avg('temp')))
    
    BadcarWeek = (BadCar.objects
                .annotate(week = ExtractWeek('time'))
                .values('week')
                .annotate(avg=Avg('badcar')))
    BadcarMonth = (BadCar.objects
                .annotate(month = ExtractMonth('time'))
                .values('month')
                .annotate(avg=Avg('badcar')))
    
    # Humidata.
    week = []
    humi = []
    tempw = []
    temp = []
    badcarw = []
    badcarwd = []
    badcarm = []
    badcarmd = []
    
    hummimonth = []
    humimonthdata = []
    tempmonth = []
    tempmonthdata = []
    
    for i in Humidata:
        week += [i['week']]
        humi += [i['avg_humi']]
    
    for i in Tempdata:
        tempw += [i['week']]
        temp += [i['avg_temp']]
    
    for i in HumidataMonth:
        hummimonth += [i['month']]
        humimonthdata += [i['avg_humi']]
    
    for i in TempdataMonth:
        tempmonth += [i['month']]
        tempmonthdata += [i['avg_temp']]
        
    for i in BadcarWeek:
        badcarw += [i['week']]
        badcarwd += [i['avg']]
        
    for i in BadcarMonth:
        badcarm += [i['month']]
        badcarmd += [i['avg']]
    
    res = {
        'humiweek' : week,
        'humi' : humi,
        'tempweek' : tempw,
        'temp' : temp,
        'humimonth' : hummimonth,
        'humimonthdata' : humimonthdata,
        'tempmonth' : tempmonth,
        'tempmonthdata' : tempmonthdata,
        'badcarweek' : badcarw,
        'badcarweekdata' : badcarwd,
        'badcarmonth' : badcarm,
        'badcarmonthdata' : badcarmd
    }
    return JsonResponse(res, status= 200)

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