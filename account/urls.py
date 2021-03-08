from django.urls import path
from .views import logout_account, LoginAccount, SignUpView, ChaneID

urlpatterns = [
    path('login/', LoginAccount.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', logout_account, name='logout'),
    path('id/', ChaneID.as_view(), name='change_id'),
]
