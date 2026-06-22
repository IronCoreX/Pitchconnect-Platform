from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    # This says: look for a number after 'turf/' and call it 'turf_id'
    path('turf/<int:turf_id>/', views.turf_detail, name='turf_detail'),
    path('check_availability/', views.check_availability, name='check_availability'),
    path('save_booking/', views.save_booking, name='save_booking'),
    path('matches/', views.match_list, name='match_list'),
    path('join_match/<int:match_id>/', views.join_match, name='join_match'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
]