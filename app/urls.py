from django.urls import path

from app.views import UserRegisterView, UserLoginView, ContentList, ContentDetail

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('contents/', ContentList.as_view(), name='content-list'),
    path('contents/<int:pk>/', ContentDetail.as_view(), name='content-detail'),
    path('content-search/', ContentDetail.as_view(), name='content-search')
]
