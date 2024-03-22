from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

from catalog.models import BookInstance


class SignUp(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        book_instance = BookInstance.objects.filter(borrower=self.request.user)
        context = {'book_instance': book_instance}
        return render(request, 'profile.html', context)
