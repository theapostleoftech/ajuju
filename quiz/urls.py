from django.urls import path

from quiz.views import quiz_views, quiz_creator_views, subject_creator_views

app_name = 'quiz'
# urlpatterns = [
#
#     # path('quiz/<int:pk>/', views.QuizDetailView.as_view(), name='quiz_detail'),
#
#     # path('quiz/<int:pk>/start/', views.start_quiz, name='start_quiz'),
#     # path('quiz/attempt/<int:attempt_id>/', views.take_quiz, name='take_quiz'),
#     # path('quiz/result/<int:attempt_id>/', views.quiz_result, name='quiz_result'),
# ]

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
    # path('subjects/', views.SubjectListView.as_view(), name='subject_list'),
    # path('subjects/<int:pk>/', views.SubjectDetailView.as_view(), name='subject_detail'),
    path('subjects/new/', subject_creator_views.SubjectCreateView.as_view(), name='subject_create'),
    path('subjects/update/<uuid:pk>/', subject_creator_views.SubjectUpdateView.as_view(), name='subject_update'),
    path('subjects/delete/<uuid:pk>/', subject_creator_views.SubjectDeleteView.as_view(), name='subject_delete'),

]

urlpatterns = quiz_urlpatterns + quiz_creator_urlpatterns + subject_creator_urlpatterns
