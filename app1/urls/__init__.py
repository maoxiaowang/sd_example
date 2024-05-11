from django.urls import path, include

app_name = 'app1'

urlpatterns = [
    path('person/', include('app1.urls.person')),
    path('company/', include('app1.urls.company')),
]
