from django.urls import path

from quiz.views import quiz_views, quiz_creator_views, subject_creator_views

app_name = 'quiz'

quiz_urlpatterns = [
    path('', quiz_views.QuizIndexView.as_view(), name='quiz_index'),
    path('subjects/', quiz_views.SubjectIndexView.as_view(), name='subject_index'),
]

quiz_creator_urlpatterns = [
    path('quiz/new/', quiz_creator_views.create_quiz_view, name='quiz_create'),
    path('quiz/update/<quiz_id>/', quiz_creator_views.edit_quiz_view, name='quiz_update'),
    path('quiz/delete/<uuid:pk>/', quiz_creator_views.QuizDeleteView.as_view(), name='quiz_delete'),
]

subject_creator_urlpatterns = [
    path('subjects/new/', subject_creator_views.SubjectCreateView.as_view(), name='subject_create'),
    path('subjects/update/<uuid:pk>/', subject_creator_views.SubjectUpdateView.as_view(), name='subject_update'),
    path('subjects/delete/<uuid:pk>/', subject_creator_views.SubjectDeleteView.as_view(), name='subject_delete'),

]

urlpatterns = quiz_urlpatterns + quiz_creator_urlpatterns + subject_creator_urlpatterns
