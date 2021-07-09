from django.urls import path
from dashboard.views import Index, Index2, Adjust

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('pdf', Index2.as_view(), name='index2'),
    path('adjust', Adjust.as_view(), name='adjust'),
]
