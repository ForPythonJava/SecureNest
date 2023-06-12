from django.shortcuts import render, HttpResponseRedirect, redirect
from .models import *
from django.db.models import Q
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime

# Create your views here.


def index(request):
    return render(request, "index.html")


def logout(request):
    request.session.clear()
    return HttpResponseRedirect("/login")


def contact(request):
    return render(request, "contact.html")


def signin(request):
    if request.POST:
        email = request.POST["email"]
        passw = request.POST["password"]
        print(email)
        print(passw)
        user = authenticate(username=email, password=passw)
        print(user)
        if user is not None:
            login(request, user)
            if user.userType == "Admin":
                messages.info(request, "Login Success")
                return redirect("/adminHome")
            elif user.userType == "Child":
                id = user.id
                request.session["uid"] = id
                messages.info(request, "Login Success")
                return redirect("/childHome")
            elif user.userType == "School":
                id = user.id
                request.session["uid"] = id
                messages.info(request, "Login Success")
                return redirect("/userHome")
        else:
            print("Hiii")
            messages.error(request, "Invalid Username/Password")
    return render(request, "COMMON/login.html")


def studRegister(request):
    schoolData = School.objects.all()
    current_date = datetime.today().strftime("%Y-%m-%d")
    if request.POST:
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        dob = request.POST["dob"]
        gender = request.POST["gender"]
        password = request.POST["password"]
        school = request.POST["school"]
        sid = School.objects.get(id=school)
        address = request.POST["address"]
        if Login.objects.filter(username=email).exists():
            messages.error(request, "Email Already Exists")
        else:
            logUser = Login.objects.create_user(
                username=email,
                password=password,
                userType="Child",
                viewPass=password,
                is_active=1,
            )
            logUser.save()
            regChild = Child.objects.create(
                name=name,
                email=email,
                phone=phone,
                dob=dob,
                gender=gender,
                school=sid,
                address=address,
            )
            regChild.save()
            messages.success(request, "Registered Successfully")
    return render(
        request,
        "COMMON/studRegister.html",
        {"current_date": current_date, "schoolData": schoolData},
    )


def schoolReg(request):
    if request.POST:
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        state = request.POST["state"]
        address = request.POST["address"]
        password = request.POST["password"]
        if Login.objects.filter(username=email).exists():
            messages.error(request, "Email Already Exists")
        else:
            logQry = Login.objects.create_user(
                username=email,
                password=password,
                userType="School",
                viewPass=password,
                is_active=0,
            )
            logQry.save()
            schoolregQry = School.objects.create(
                name=name,
                email=email,
                phone=phone,
                address=address,
                loginid=logQry,
                state=state,
            )
            schoolregQry.save()
            messages.success(request, "Registered Successfully")
    return render(request, "COMMON/schoolReg.html")


def adminHome(request):
    return render(request, "ADMIN/adminHome.html")


def childHome(request):
    return render(request, "CHILD/childHome.html")


def schoolHome(request):
    return render(request, "SCHOOL/schoolHome.html")


def policeHome(request):
    return render(request, "POLICE/policeHome.html")


# ********************************ADMIN*****************************************


def viewChild(request):
    childData = Child.objects.all()
    return render(request, "ADMIN/viewChild.html", {"childData": childData})


def adminBase(request):
    return render(request, "ADMIN/adminBase.html")


def deleteChild(request):
    id = request.GET["id"]
    deleteStud = Child.objects.filter(id=id).delete()
    return HttpResponseRedirect("/viewChild")


def chat(request):
    uid = request.session["uid"]
    print(uid)
    sid = Child.objects.get(loginid=uid)
    time = datetime.now().time()
    date = datetime.now().date()
    formatted_time = time.strftime("%I:%M %p")
    formatted_date = date.strftime("%B %d")

    chats = Message.objects.filter(sender_id__loginid_id=uid)
    print(chats)

    if request.POST:
        message = request.POST["message"]
        sendMsg = Message.objects.create(
            message=message,
            date=formatted_date,
            time=formatted_time,
            type="Child",
            sender=sid,
        )
        sendMsg.save()
    return render(request, "ADMIN/chat.html", {"chats": chats})
