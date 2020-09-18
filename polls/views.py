from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Choice, Course, Result, Article

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
    correct_answers = request.session.get('correct')
    total_questions = request.session.get('q_amount')

    return render(request, 'polls/res.html', {'course': course,'result':results_data[k-1],'correct_answers':correct_answers,'total_questions':total_questions})

def vote(request, course_id):
    course = Course.objects.get(id=course_id)
    choices = Choice.objects.all()
    questions = course.question_set.all()
    selected_choices = dict(request.POST)
    del selected_choices['csrfmiddlewaretoken']
    print(selected_choices)
    if len(selected_choices) < len(questions):
        # Redisplay the question voting form.
        return render(request, 'polls/cv.html', {
            'course': course,
            'error_message': "Вы не ответили на все вопросы",'choices':choices,
        })
    else:
        score = 0
        correct = 0
        for key, value in selected_choices.items():
            score += int(value[0])
            if int(value[0]) is not 0:
                correct +=1
        request.session['correct'] = correct
        request.session['q_amount'] = len(questions)
        res_dict = {'correct':correct,'q_amount':len(questions)}
        return HttpResponseRedirect(reverse('polls:results', args=(course.id,score)))

def read_article(request, article_id):
    article = Article.objects.get(id=article_id)
    return render(request, 'polls/article.html', {'article':article})