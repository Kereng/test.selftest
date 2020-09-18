from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from .models import Question, Choice, Course, Result, Article

class QChoiceInline(NestedStackedInline):
    model = Choice
    fk_name = 'level'
    extra = 0


class ChoiceInline(NestedStackedInline):
    model = Question
    inlines = [QChoiceInline]
    extra = 1

class ResultsInline(NestedStackedInline):
    model = Result
    extra = 0

class QuestionAdmin(NestedModelAdmin):
    fieldsets = [
        (None,               {'fields': ['course_title','about','description','author','help_article']}),
        ('Дата', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline,ResultsInline,]
    list_display = ('course_title', 'pub_date')
    search_fields = ['course_title']

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('article_title', 'date', 'author')

admin.site.register(Course, QuestionAdmin)
admin.site.register(Article, ArticleAdmin)


