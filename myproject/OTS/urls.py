from django.urls import path
from OTS.views import *
app_name='OTS'
urlpatterns = [
    path('',welcome ),
    path('new-candidate',candidateRegistrationForm,name='registrationForm'),
    path('store-candidate',candidateRegistration,name='storecandidate'),
    path('login',loginView,name='login'),
    path('home',candidateHome,name='home'),
    path('test-paper',testPaper,name='testPaper'),
    path('calculate-result',calculateTestResult,name='calculateTest'),
    path('test-history',testResultHistory,name='testhistory'),
    path('result',showTextResult,name='result'),
    path('logout',logoutView,name='logout'),
]