from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('events/<int:event_id>/', views.events_detail, name='detail'),
    path('events/create/', views.EventCreate.as_view(), name='events_create'),
    path('events/<int:pk>/update/', views.EventUpdate.as_view(), name='events_update'),
    path('events/<int:pk>/delete/', views.EventDelete.as_view(), name='events_delete'),
    path('events/<int:event_id>/add_photo/', views.add_photo, name='add_photo'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('login_redirect/', views.login_redirect, name='login_redirect'),
    path('events/type/<str:type>', views.events_by_type, name='events_by_type'),
    path('events/all', views.events_all, name='events_all'),
    path('event/<int:event_id>/delete/', views.delete_event, name='event_delete'),
    
    

]