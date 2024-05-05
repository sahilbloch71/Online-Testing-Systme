from django.urls import path
from OTS.views import *

urlpatterns = [
    path('',welcome ),
    path('new-candidate',candidateRegistrationForm),
    path('store-candidate',candidateRegistration),
    path('login',loginView),
    path('home',candidateHome),
    path('test-paper',testPaper),
    path('calculate-result',calculateTestResult),
    path('test-history',testResultHistory),
    path('result',showTextResult),
    path('logout',logoutView),
]