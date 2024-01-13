from django.shortcuts import render
from .models import Organization
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class OrganizationCreateView(LoginRequiredMixin, CreateView):
    model = Organization
    template_name = 'organizations/organization_form.html'
    fields = ['name', 'city']

    def form_valid(self, form): #TODO
        
        return super().form_valid(form)


class OrganizationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Organization
    template_name = 'organizations/organization_form.html'
    fields = ['name', 'city']

    def test_func(self):
        organization = self.get_object()
        return 0 #TODO


class OrganizationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Organization
    template_name = 'organizations/delete_confirm.html'
    success_url = '/'

    def test_func(self):
        organization = self.get_object()
        return 0 #TODO