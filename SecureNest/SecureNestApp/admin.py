from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Login)
admin.site.register(School)
admin.site.register(Child)
admin.site.register(Message)
admin.site.register(Complaints)
admin.site.register(SchoolComplaints)
