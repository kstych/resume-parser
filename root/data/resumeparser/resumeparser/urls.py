from django.urls import path
from dashboard.views import Index
urlpatterns = [
    path('', Index.as_view(), name='index')
]
