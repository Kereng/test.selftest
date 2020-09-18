from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:course_id>/', views.detail, name='detail'),
    path('<int:course_id>/results/<int:score>', views.results, name='results'),
    path('<int:course_id>/vote/', views.vote, name='vote'),
    path('read/<int:article_id>',views.read_article, name='article')
]