from django.contrib import admin
from .models import  Quiz,Question,Option


# Register your models here.



class OptionAdmin(admin.StackedInline):
    model = Option


class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionAdmin,]

admin.site.register(Question,QuestionAdmin)
admin.site.register(Quiz)
#admin.site.register(Option)