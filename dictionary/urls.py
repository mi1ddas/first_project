from django.urls import path
from .views import IndexView, AddTermView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('add/', AddTermView.as_view(), name='add_term'), 
]