from django.urls import path
from .views import base, teacher_panel, login, signup

urlpatterns = [
    path('', base, name='base'),
    path('teacher/', teacher_panel, name='teacher_panel'),
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
]
