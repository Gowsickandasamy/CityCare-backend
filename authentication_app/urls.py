from authentication_app import views
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns=[
    path('register/',views.register_user, name='register_user'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user-info/',views.UserProfileView.as_view(),name = 'userProfile'),
    path('change-password/',views.ChangePasswordView.as_view(), name='change_password'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]