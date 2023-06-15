from django.shortcuts import (
    render,
    HttpResponseRedirect,
    redirect,
    HttpResponsePermanentRedirect,
)
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
    messages.success(request, "Logged Out")
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
                id = user.id
                request.session["uid"] = id
                request.session["type"] = "Admin"
                messages.info(request, "Login Success")
                return redirect("/adminHome")
            elif user.userType == "Child":
                id = user.id
                request.session["uid"] = id
                request.session["type"] = "Child"
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
    uid = request.session["uid"]
    print(uid)
    return render(request, "ADMIN/adminHome.html")


def childHome(request):
    return render(request, "CHILD/childHome.html")


def schoolHome(request):
    return render(request, "SCHOOL/schoolHome.html")


def policeHome(request):
    return render(request, "POLICE/policeHome.html")


# ********************************ADMIN*****************************************


def viewChild(request):
    childData = Child.objects.exclude(name="Admin")
    return render(request, "ADMIN/viewChild.html", {"childData": childData})


def adminBase(request):
    return render(request, "ADMIN/adminBase.html")


def deleteChild(request):
    id = request.GET["id"]
    deleteStud = Child.objects.filter(id=id).delete()
    return HttpResponseRedirect("/viewChild")


def chat(request):
    uid = request.session["uid"]
    type = request.session["type"]
    aid = Child.objects.get(name="Admin")
    sid = Child.objects.get(loginid=uid)
    time = datetime.now().time()
    date = datetime.now().date()
    formatted_time = time.strftime("%I:%M %p")
    formatted_date = date.strftime("%B %d")
    ccid = request.GET["id"]
    childid = Child.objects.get(id=ccid)

    chats = Message.objects.filter(
        Q(sender_id__loginid_id=uid) | Q(receiver_id__loginid=uid)
    )

    print("Chats", chats)
    print(uid)

    if request.POST:
        message = request.POST["message"]
        if type == "Child":
            sendMsg = Message.objects.create(
                message=message,
                date=formatted_date,
                time=formatted_time,
                type="Child",
                sender=sid,
                receiver=aid,
            )
            sendMsg.save()
        elif type == "Admin":
            sendMsg = Message.objects.create(
                message=message,
                date=formatted_date,
                time=formatted_time,
                type="Admin",
                sender=aid,
                receiver=childid,
            )
            sendMsg.save()
    return render(request, "ADMIN/chat.html", {"chats": chats})


# def viewStudents(request):
#     lis=[]
#     getData=''
#     childData = Message.objects.values('sender').distinct()

#     for data in childData:
#         print(data['sender'])
#         lis.append(data['sender'])
#     print(lis)
#     for i in lis:
#         getData=Child.objects.filter(id=i)
#     print(getData)
#     return render(request,"ADMIN/viewStudents.html",{"childData":childData,"getData":getData})


def viewStudents(request):
    common_ids = set(Child.objects.values_list("id", flat=True)).intersection(
        Message.objects.values_list("sender", flat=True)
    )
    common_children = Child.objects.filter(id__in=common_ids).exclude(name="Admin")
    common_messages = Message.objects.filter(id__in=common_ids)
    print(common_children)
    for child in common_children:
        print(f"Child ID: {child.id}, Child Name: {child.name}")
    return render(
        request, "ADMIN/viewStudents.html", {"common_children": common_children}
    )


def replyChat(request):
    aid = Child.objects.get(name="Admin")
    id = request.GET["id"]
    print(id)
    sid = Child.objects.get(id=id)
    time = datetime.now().time()
    date = datetime.now().date()
    formatted_time = time.strftime("%I:%M %p")
    formatted_date = date.strftime("%B %d")
    # Messages
    chatdata = Message.objects.filter(
        Q(receiver_id=3) & Q(sender_id=id) | Q(receiver_id=id) & Q(sender_id=3)
    ).order_by("time")
    print("test", chatdata)
    if request.POST:
        message = request.POST["message"]
        sendMsg = Message.objects.create(
            message=message,
            date=formatted_date,
            time=formatted_time,
            type="Admin",
            sender=aid,
            receiver=sid,
        )
        sendMsg.save()
    return render(request, "ADMIN/replyChat.html", {"chats": chatdata})


def addLaws(request):
    if request.POST:
        actname = request.POST["actname"]
        year = request.POST["actyear"]
        desc = request.POST["desc"]
        addLaw = Laws.objects.create(actname=actname, year=year, desc=desc)
        addLaw.save()
        messages.success(request, "Added Successfully")
        # return redirect("/viewLaws")
    return render(request, "ADMIN/addLaws.html")


def addRights(request):
    if request.POST:
        rightname = request.POST["rightname"]
        desc = request.POST["desc"]
        addRight = Rights.objects.create(rightname=rightname, desc=desc)
        addRight.save()
    return render(request, "ADMIN/addRights.html")


def viewLaws(request):
    laws = Laws.objects.all()
    return render(request, "ADMIN/viewLaws.html", {"laws": laws})


def viewRights(request):
    rights = Rights.objects.all()
    return render(request, "ADMIN/viewRights.html", {"rights": rights})


def viewSchool(request):
    schoolData = School.objects.all()
    return render(request, "ADMIN/viewSchool.html", {"schoolData": schoolData})


def deleteSchool(request):
    id = request.GET["id"]
    deleteData = Login.objects.get(id=id).delete()
    return HttpResponsePermanentRedirect("/viewSchool")


def manageSchool(request):
    id = request.GET["id"]
    status = request.GET["status"]
    data = Login.objects.get(id=id)
    data.is_active = status
    data.save()
    return HttpResponsePermanentRedirect("/viewSchool")


def addPoliceStation(request):
    if request.POST:
        stname = request.POST["stname"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        district = request.POST["district"]
        address = request.POST["address"]
        password = request.POST["password"]

        addLogin = Login.objects.create_user(
            username=email,
            password=password,
            userType="Police",
            viewPass=password,
            is_active=1,
        )
        addLogin.save()
        addPolice = PoliceStation.objects.create(
            name=stname,
            email=email,
            phone=phone,
            district=district,
            address=address,
            loginid=addLogin,
        )
        addPolice.save()
        messages.success(request, "Added Successfully")
        return HttpResponsePermanentRedirect("/viewPolice")
    return render(request, "ADMIN/addPoliceStation.html")


def viewPolice(request):
    policeData = PoliceStation.objects.all()
    return render(request, "ADMIN/viewPolice.html", {"policeData": policeData})


def deletePolice(request):
    id = request.GET["id"]
    deleteData = Login.objects.get(id=id).delete()
    return HttpResponsePermanentRedirect("/viewPolice")


#################################CHILDREN##############################################
def childViewLaws(request):
    laws = Laws.objects.all()
    return render(request, "CHILD/viewLaws.html", {"laws": laws})


def childViewRights(request):
    rights = Rights.objects.all()
    return render(request, "CHILD/viewRights.html", {"rights": rights})
