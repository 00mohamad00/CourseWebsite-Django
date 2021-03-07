from django.urls import path
from .views import index, courses, HomeworkCreate, HomeworkUpdate, HomeworkDelete,\
    HomeworkAnswers, AnswerScoreUpdate, CourseAsTeacher, ContentCreate, ContentDelete, CourseAsStudnet, HomeworkView,\
    AnswerUpdate, CourseCreate

urlpatterns = [
    path('', index, name='index'),
    path('courses/', courses, name='courses'),

    path('course/add/', CourseCreate.as_view(), name='course_create'),

    path('course/t/<int:pk>/', CourseAsTeacher.as_view(), name='course_as_teacher'),
    path('course/t/<int:pk>/homework/add/', HomeworkCreate.as_view(), name='homework_create'),
    path('course/t/<int:pk>/homework/<int:pk2>/update', HomeworkUpdate.as_view(), name='homework_update'),
    path('course/t/<int:pk>/homework/<int:pk2>/delete', HomeworkDelete.as_view(), name='homework_delete'),
    path('course/t/<int:pk>/homework/<int:pk2>/answers', HomeworkAnswers.as_view(), name='homework_answers'),
    path('course/t/<int:pk>/homework/<int:pk2>/answers/<int:pk3>/score/change', AnswerScoreUpdate.as_view(), name='homework_answers_update'),
    path('course/t/<int:pk>/content/add', ContentCreate.as_view(), name='content_create'),
    path('course/t/<int:pk>/content/<int:pk2>/delete', ContentDelete.as_view(), name='content_delete'),

    path('course/<int:pk>/', CourseAsStudnet.as_view(), name='course_as_student'),
    path('course/<int:pk>/homework/<int:pk2>/', HomeworkView.as_view(), name='homework_view'),
    path('course/<int:pk>/homework/<int:pk2>/answer/<int:pk3>/update', AnswerUpdate.as_view(), name='answer_update'),
]
