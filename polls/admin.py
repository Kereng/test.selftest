from django.contrib import admin

from .models import Question, Choice, Course, Result

class ChoiceInline(admin.TabularInline):
    model = Question
    extra = 1

class ResultsInline(admin.TabularInline):
    model = Result
    extra = 2

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['course_title','about','description','author']}),
        ('Дата', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline,ResultsInline]
    list_display = ('course_title', 'pub_date')
    search_fields = ['course_title']
admin.site.register(Course, QuestionAdmin)
admin.site.register(Choice)

