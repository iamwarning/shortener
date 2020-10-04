from django.urls import path
from .views import CreateShortener, LinkPage, LinkRedirect

app_name = 'short'

urlpatterns = [
    path('', CreateShortener.as_view(), name='index'),
    path('<int:pk>/', LinkPage.as_view(), name='detail'),
    path('<str:code>/', LinkRedirect.as_view(), name='redirect'),
]