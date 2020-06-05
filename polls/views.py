from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Choice, Course, Result

def index(request):

    courses = Course.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]
    return render(request, 'polls/projects-no-images.html',{'latest_courses_list':courses})

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_courses_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Course.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


#class DetailView(generic.DetailView):
#    model = Course
#    template_name = 'polls/detail.html'
#    def get_choices(self):
#        return Choice.objects.all()

def detail(request, course_id):
    course = Course.objects.get(id=course_id)
    choices = Choice.objects.all()
    return render(request, 'polls/cv.html', {'course': course,'choices':choices})

def results(request, course_id, score):

    course = Course.objects.get(id=course_id)
    results_data = course.result_set.all().order_by('target')
    k=0
    for r in results_data:
        if int(score) >= int(r.target):
            k+=1

    return render(request, 'polls/res.html', {'course': course,'result':results_data[k-1]})

def vote(request, course_id):
    course = Course.objects.get(id=course_id)
    choices = Choice.objects.all()
    questions = course.question_set.all()
    print(questions)
    selected_choices = dict(request.POST)
    del selected_choices['csrfmiddlewaretoken']

    print(selected_choices)
#<QueryDict: {'csrfmiddlewaretoken': ['6MDdCocIDhd7VgYXu1e1tHDrkyRxAFdkja5onsc5BkksCjGzvHohflaiSltsicrW'], 'question1': ['3'], 'question2': ['1']}>

    if len(selected_choices) < len(questions):
        # Redisplay the question voting form.
        return render(request, 'polls/cv.html', {
            'course': course,
            'error_message': "Вы не ответили на все вопросы",'choices':choices,
        })
    else:

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        score = 0
        for key, value in selected_choices.items():
            score += int(value[0])

        return HttpResponseRedirect(reverse('polls:results', args=(course.id,score)))