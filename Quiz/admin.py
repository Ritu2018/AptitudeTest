from django.contrib import admin
from .models import  Quiz,Question,Option,Profile,Answers
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

# Register your models here.



class OptionAdmin(NestedStackedInline):
    model = Option

class QuestionAdmin(NestedStackedInline):
   model = Question
   inlines = [OptionAdmin,]



class QuizAdmin(NestedModelAdmin):
    inlines = [QuestionAdmin,]


class AnswerAdmin(admin.StackedInline):
    model = Answers

class ProfileAdmin(admin.ModelAdmin):
    inlines = [AnswerAdmin,]

admin.site.register(Quiz,QuizAdmin)
#admin.site.register(Question,QuestionAdmin)

admin.site.register(Profile, ProfileAdmin)