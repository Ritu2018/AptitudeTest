from django.contrib import admin
from .models import  Quiz,Question,Option
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

# Register your models here.



class OptionAdmin(NestedStackedInline):
    model = Option

class QuestionAdmin(NestedStackedInline):
   model = Question
   inlines = [OptionAdmin,]



class QuizAdmin(NestedModelAdmin):
    inlines = [QuestionAdmin,]

admin.site.register(Quiz,QuizAdmin)
#admin.site.register(Question,QuestionAdmin)

#admin.site.register(Option)