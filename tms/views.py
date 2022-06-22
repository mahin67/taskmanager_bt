from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import auth

from .models import SWorker,App_models,work_type,User,worker_role


# Create your views here.
def home(request):
    return render(request, 'Log_in.html')
def dash(request):

    return render(request, 'dashboard.html')

def login(request):
    print(" mahin called")
    role=worker_role.objects.all()
    use=User.objects.all()
    use_role=False

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        for names in role:
            for user in use:
                if user.email==username and names.role_id_id==user.id and names.is_Lmanager== True:
                    use_role=True
                else :
                    use_role=False
        print(username)
        print(password)
        user =  auth.authenticate(username=username,password=password)
        print('user details',user)

        if user is not  None:
            if use_role==True:
                user.is_staff = True
                user.save()
                auth.login(request, user)
                return redirect("/dashboard_manager")
            else:
                user.is_staff=True
                user.save()
                auth.login(request,user)
                return  redirect("/dashboard")
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('/loginview')

def manager_login(request):
    result = {
    }
    print('result-primes',result)
    rs_list=[]
    post_wlist = SWorker.objects.all()
    names_list= User.objects.all()
    app_list= App_models.objects.all()


    for names in post_wlist:
        for res in names_list:
            if res.id==names.name_id and names.permission_status == False and names.work_status == True:
                work_date=str(names.work_time)
                work_dur=str(names.time)
                app_name = App_models.objects.get(id=names.app_name_id)
                #print('APp name',app_name.app_name)
                result["ID"]=names.id
                result["Full_name"] = (res.first_name + ' ' + res.last_name)
                result["App_name"] = app_name.app_name
                result["Work_name"]=names.work_name
                result["Work_desc"]=names.work_descp
                result["Work_date"]=work_date
                result["Duration"] = names.time

                rs_list.append(result.copy())
                #print('result',rs_list)
    print('my list',rs_list)


    if request.method == 'POST':
        print("POST called-------",request.POST.get('SApprove'))
        rs_list=[]
        rs_dict={}
        if request.POST.get('SApprove') is not None :
            id_val=request.POST.get('Id-val')

            for result in post_wlist:
                print(type(result.id))
                if result.id == int(id_val):
                    print(result.permission_status)
                    result.permission_status=True
                    result.save()

            for names in post_wlist:
                print('hello1')
                for res in names_list:
                    print('hello2')
                    if res.id == names.name_id and names.permission_status == False and names.work_status == True:
                        work_date = str(names.work_time)
                        work_dur = str(names.time)
                        app_name = App_models.objects.get(id=names.app_name_id)
                        print('APp name',app_name.app_name)
                        rs_dict["ID"] = names.id
                        rs_dict["Full_name"] = (res.first_name + ' ' + res.last_name)
                        rs_dict["App_name"] = app_name.app_name
                        rs_dict["Work_name"] = names.work_name
                        rs_dict["Work_desc"] = names.work_descp
                        rs_dict["Work_date"] = work_date
                        rs_dict["Duration"] = names.time
                        #
                        rs_list.append(rs_dict.copy())

            return render(request, 'dashboard_manager.html',
                          {"result": rs_list})

        else:
            return render(request, 'dashboard_manager.html',
                          { "result" : rs_list })

    #rs_list.append(result)
    # print("result", result)

    return render(request, 'dashboard_manager.html',{ "result" : rs_list })

def logout(request):
    user=auth.get_user(request)
    user.is_staff=False
    user.save()
    print(user)
    auth.logout(request)
    messages.info(request, 'Logout Success')
    return redirect('/')

def work_entry(request):
    # print(" mahin called work")

    user = auth.get_user(request)
    use1= user.get_username()
    use2=User.objects.all()

    #print(type(use2))

    full_name=0

    for  name in use2:
        # print('Firs name: ', name.email)
        # print('username: ', use1)
        if name.email == use1:
            # print('Second name: ', name.first_name)
            # full_name= str(name.first_name)+' '+str(name.last_name)
            full_name=name.id

    print('FUll name: ',full_name)
    app_list=App_models.objects.all()
   # print('work_list---',app_list)

    work_list = work_type.objects.all()
   # print('work_list---', work_list)

    post_wlist=SWorker.objects.all()

    User_name={
        "user_id":full_name
    }


    print("type of user_name",type(full_name))

    # print('User ---', use1)
    if request.method == 'POST':
        print("Post called")
        task_date=request.POST['tdate']
        app_name = request.POST['appname']
        work_name= request.POST['work_desc']
        det_desc = request.POST['wdesc']
        days=request.POST['day']
        time_format=''
        if int(days) >59 :
            d=int(days)/60
            time_format=str(round(d))+' Mins'
            print('minutes ',round(d))
            if d>59 :
                d=d/60
                time_format = str(round(d)) + ' Hrs'
                print('hours',round(d))
                if d > 23:
                    d = d / 24
                    time_format = str(round(d,2)) + ' Days'
                    print('days', round(d,2))

        print(time_format)
        print('App_name +',app_name)
        print('work_name +', work_name)
        print('Time duration',days)
        if days !="":
            ins = SWorker(name_id=full_name,app_name_id=app_name,work_name=work_name, work_descp=det_desc,work_time=task_date,time=time_format)
            ins.save()
            print(time_format, '=====days')
            redirect('/workform')

    elif request.method == 'GET':
        print("Get called-------",request.GET.get('specbtn'))
        if request.GET.get('specbtn') is not None :
            print('specbtn called')
            for result in post_wlist:
                print(result.work_status)
                for name in use2:
                    if name.id == result.name_id:
                        if name.email== use1:
                            print('Result Saved')
                            result.work_status=True
                            result.save()

            return render(request, 'register_work.html',
                   {"App_models": app_list, "work_type": work_list, "SWorker": post_wlist, "User_id": full_name})

        else:
            return render(request, 'register_work.html',
                          {"App_models": app_list, "work_type": work_list, "SWorker": post_wlist,"User_id":full_name})

    return render(request, 'register_work.html',{"App_models":app_list , "work_type":work_list ,"SWorker":post_wlist,"User_id":full_name})



# def manager_dashboard(request):
#     result=''
#
#     return render(request,'dashboard_manager.html',{" result ":result})

