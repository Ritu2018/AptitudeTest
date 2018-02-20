from django.contrib import admin
from .models import  Quiz
from .models import Question
from .models import Option

# Register your models here.
admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(Option)