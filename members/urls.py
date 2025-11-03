from django.urls import path
from .views import ProfileDetailView, ProfileUpdateView, MyProfileView

urlpatterns = [
    path('profile/<uuid:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/edit/', ProfileUpdateView.as_view(), name ="edit_profile"),
    path('profile/', MyProfileView.as_view(), name='my_profile'),  # New
]
