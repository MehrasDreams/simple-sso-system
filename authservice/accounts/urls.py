from django.urls import path, include
from .views import *

app_name = 'Auth'

urlpatterns = [
    path('token/', ObtainTokenView.as_view(), name='login'),
    path('verify/', VerifyApiView.as_view(), name='Verify'),
    path('send-code/', SendCode.as_view(), name='SendCode'),

]
