from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import (LoginRequiredMixin, 
                                        UserPassesTestMixin, 
                                        PermissionRequiredMixin
                                        )

from django.views.generic.edit import FormView
from django.views.generic.detail import SingleObjectMixin  # Correct import
from django.urls import reverse_lazy, reverse
from .models import Book, Review
from .forms import ReviewForm
from django.db.models import Q

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

class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = "book/review_form.html"

    def get_success_url(self):
        return reverse_lazy("book_detail", kwargs={"pk": self.object.book.pk})

    def test_func(self):
        review = self.get_object()
        # Only the author or admin can edit
        return self.request.user == review.author or self.request.user.is_superuser


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = "book/review_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("book_detail", kwargs={"pk": self.object.book.pk})

    def test_func(self):
        review = self.get_object()
        # Only the author or admin can delete
        return self.request.user == review.author or self.request.user.is_superuser
    
    
    
# ----------------------------------------------------------
# 4️⃣ Book Detail View (combine GET + POST behavior)
# ----------------------------------------------------------
"""class BookDetailView(DetailView):
    model = Book
    template_name = 'book/book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReviewForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = self.object
            review.author = request.user
            review.save()
            return redirect('book_detail', pk=self.object.pk)
        
        context = self.get_context_data(form=form)
        return self.render_to_response(context)"""
        
class BookDetailView(PermissionRequiredMixin, DetailView):
    model = Book
    context_object_name = "book"
    template_name = "book/book_detail.html"
    login_url = "account_login"
    permission_required = "bookinfo.special_status"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()

        # Handle edit mode
        edit_id = self.request.GET.get("edit")
        if edit_id:
            review_to_edit = book.reviews.filter(id=edit_id, author=self.request.user).first()
            if review_to_edit:
                from .forms import ReviewForm
                context["form"] = ReviewForm(instance=review_to_edit)
                context["edit_review_id"] = review_to_edit.id
        else:
            from .forms import ReviewForm
            context["form"] = ReviewForm()

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        book = self.object
        from .forms import ReviewForm

        # Check if editing an existing review
        edit_id = request.GET.get("edit")
        if edit_id:
            review = book.reviews.filter(id=edit_id, author=request.user).first()
            form = ReviewForm(request.POST, instance=review)
        else:
            form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.author = request.user
            review.save()
            return redirect("book_detail", pk=book.pk)

        context = self.get_context_data(form=form)
        return self.render_to_response(context)
    
    # ----------------------------------------------------------
# Search Book
# ----------------------------------------------------------
class SearchListView(ListView):
    model = Book
    context_object_name = "book_list"
    template_name = "book/book_search.html"
    
    #get request to search book
    def get_queryset(self):
        query = self.request.GET.get("q")
        
        if query:
            return Book.objects.filter(
                Q(title__icontains=query) | Q(author__icontains = query)
            ).distinct()
            
        return Book.objects.none()