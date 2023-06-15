"""
URL configuration for SecureNest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from SecureNestApp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("index/", views.index),
    path("", views.index),
    path("login/", views.signin),
    path("studRegister/", views.studRegister),
    path("schoolReg/", views.schoolReg),
    path("contact/", views.contact),
    path("adminHome/", views.adminHome),
    path("childHome/", views.childHome),
    path("schoolHome/", views.schoolHome),
    path("viewChild/", views.viewChild),
    path("adminBase/", views.adminBase),
    path("logout/", views.logout),
    path("deleteChild/", views.deleteChild),
    path("chat/", views.chat),
    path("viewStudents/", views.viewStudents),
    path("replyChat/", views.replyChat),
    path("addLaws/", views.addLaws),
    path("addRights/", views.addRights),
    path("viewLaws/", views.viewLaws),
    path("viewRights/", views.viewRights),
    path("childViewLaws/", views.childViewLaws),
    path("childViewRights/", views.childViewRights),
    path("viewSchool/", views.viewSchool),
    path("manageSchool/", views.manageSchool),
    path("deleteSchool/", views.deleteSchool),
    path("addPoliceStation/", views.addPoliceStation),
    path("viewPolice/", views.viewPolice),
    path("deletePolice/", views.deletePolice),
]
