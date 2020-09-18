from django.db import models
import datetime
from django.utils import timezone
from ckeditor.fields import RichTextField




class Course(models.Model):
    course_title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('Дата публикации')
    author = models.CharField(max_length=200)
    about = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    help_article = models.ForeignKey('Article',on_delete=models.CASCADE)

    def __str__(self):
        return self.course_title

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Question(models.Model):
    level = models.ForeignKey(Course, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    level = models.ForeignKey('Question',on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class Result(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    target = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)

class Article(models.Model):
    article_title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    date = models.DateTimeField('Дата публикации')
    content = RichTextField()
    def __str__(self):
        return self.article_title