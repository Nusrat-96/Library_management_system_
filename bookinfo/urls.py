from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookListView.as_view(), name='book_list'),
    path("<uuid:pk>", views.BookDetailView.as_view(), name="book_detail"),
    path("review/<int:pk>/edit/", views.ReviewUpdateView.as_view(), name="review_edit"),
    path("review/<int:pk>/delete/", views.ReviewDeleteView.as_view(), name="review_delete"),
]
