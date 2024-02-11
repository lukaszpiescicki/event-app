from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django.views.generic.list import ListView

from .models import Organization


class OrganizationsListView(ListView):
    model = Organization
    template_name = "organizations/organizations.html"
    context_object_name = "organizations"


class OrganizationsDetailView(DetailView):
    model = Organization
    template_name = "organizations/organization.html"


class OrganizationCreateView(LoginRequiredMixin, CreateView):
    model = Organization
    template_name = "organizations/organization_form.html"
    fields = ["name", "city"]
    permission_required = "organizations.add_organization"


class OrganizationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Organization
    template_name = "organizations/organization_form.html"
    fields = ["name", "city"]
    permission_required = "organizations.update_organization"


class OrganizationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Organization
    template_name = "organizations/delete_confirm.html"
    success_url = "/"
