from django.urls import path
from .views import base, login_account, signup, logout_account

urlpatterns = [
    path('', base, name='base'),
    path('login/', login_account, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', logout_account, name='logout'),
]
