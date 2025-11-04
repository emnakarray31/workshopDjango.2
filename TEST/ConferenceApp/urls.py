from django.urls import path
from . import views

urlpatterns = [
    path('liste/', views.list_conferences, name='list_conferences'),
    path('<int:pk>/', views.conferencedetail.as_view(), name='conferencedetail'),
    path('add/', views.conferenceCreate.as_view(), name='add_conference'),
    path('update/<int:pk>/', views.conferenceUpdate.as_view(), name='edit_conference'),
    path('delete/<int:pk>/', views.conferenceDelete.as_view(), name='conference_delete'),
]
