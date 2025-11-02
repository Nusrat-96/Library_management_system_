from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.views.generic.detail import SingleObjectMixin  # Correct import
from django.urls import reverse
from .models import Book, Review
from .forms import ReviewForm


# ----------------------------------------------------------
# 1️⃣ Book List
# ----------------------------------------------------------
class BookListView(ListView):
    model = Book
    context_object_name = "book_list"
    template_name = "book/book_list.html"


# ----------------------------------------------------------
# 2️⃣ Review Get - show book details and review form
# ----------------------------------------------------------
class ReviewGet(DetailView):  
    model = Book
    template_name = "book/book_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ReviewForm()
        return context


# ----------------------------------------------------------
# 3️⃣ Review Post - handle review submission
# ----------------------------------------------------------
class ReviewPost(SingleObjectMixin, FormView):
    model = Book
    form_class = ReviewForm
    template_name = "book/book_detail.html"
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Get Book instance
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        review = form.save(commit=False)
        review.book = self.object
        review.author = self.request.user
        review.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        # ✅ Correct way: use the book’s id, not self.id
        return reverse("book_detail", args=[str(self.object.id)])


# ----------------------------------------------------------
# 4️⃣ Book Detail View (combine GET + POST behavior)
# ----------------------------------------------------------
class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    context_object_name = "book"
    template_name = "book/book_detail.html"
    login_url = "account_login"

    def get(self, request, *args, **kwargs):
        # show book + form
        view = ReviewGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # handle form submission
        view = ReviewPost.as_view()
        return view(request, *args, **kwargs)
