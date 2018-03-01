from django.contrib import admin
from .models import Quiz, Question, Option, Profile, Answers, Result
from nested_inline.admin import NestedStackedInline, NestedModelAdmin


# Register your models here.



class OptionAdmin(NestedStackedInline):
    model = Option


class QuestionAdmin(NestedStackedInline):
    model = Question
    inlines = [OptionAdmin, ]


class QuizAdmin(NestedModelAdmin):
    inlines = [QuestionAdmin, ]


class AnswerAdmin(admin.StackedInline):
    model = Answers


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    ordering = ('-score',)
    list_display = ('profile', 'score')
    list_filter = ('quiz',)

    def profile(self, obj):
        return obj.profile

        # profile.admin_order_field = '-score'


# class ProfileAdmin(admin.ModelAdmin):
#    inlines = [AnswerAdmin,]

admin.site.register(Quiz, QuizAdmin)
# admin.site.register(Question,QuestionAdmin)

admin.site.register(Profile)


@admin.register(Answers)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('profile', 'right', 'option', 'question')
