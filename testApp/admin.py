from django.contrib import admin

# Register your models here.
from .models import Case,CaseImages
admin.site.register(Case)
admin.site.register(CaseImages)
