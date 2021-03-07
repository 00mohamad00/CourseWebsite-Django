from django.urls import path
from .views import signup, logout_account, LoginAccount, SignUpView

urlpatterns = [
    path('login/', LoginAccount.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', logout_account, name='logout'),
]
