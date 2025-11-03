# members/views.py
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView
from django.urls import reverse_lazy
from .models import Member

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Member
    template_name = 'members/profile_detail.html'
    context_object_name = 'member'

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Member
    template_name = 'members/profile_update.html'
    fields = ['name', 'profile_picture', 'phone', 'address', 'date_of_birth', 'gender', 'membership_type']

    def get_object(self, queryset=None):
        """Return the Member object of the currently logged-in user."""
        return self.request.user.member

    def get_success_url(self):
        return reverse_lazy('profile_detail', kwargs={'pk': self.request.user.member.pk})

class MyProfileView(View):
    def get(self, request, *args, **kwargs):
        member = request.user.member  # Assuming OneToOne relation
        return redirect('profile_detail', pk=member.pk)