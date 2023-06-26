from django.urls import path
from .views import*

urlpatterns = [
    path('google/', GoogleSocialAuthView.as_view()),
    path('accounts/<str:email>', AccountsDetailView.as_view())
]
