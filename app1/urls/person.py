from django.urls import path
from app1.views import person as views

urlpatterns = [
    path('list/', views.PersonList.as_view()),
    path('create/', views.PersonCreate.as_view()),
]
