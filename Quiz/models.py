from django.db import models

# Create your models here.
class Quiz(models.Model):
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=800,blank=True)
    dept=models.CharField(max_length=40)
    date=models.DateTimeField()
    duration=models.TimeField(blank=True)
    no_of_question=models.IntegerField(blank=True)
    theme=models.ImageField(blank=True)
    active=models.BooleanField()

class Question(models.Model):
    text=models.TextField()
    score=models.IntegerField(default=1)
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE())

class Option(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE())
    name=models.CharField(max_length=1200)
    is_correct=models.BooleanField()

