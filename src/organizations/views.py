from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
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


class OrganizationCreateView(LoginRequiredMixin, CreateView, PermissionRequiredMixin):
    model = Organization
    template_name = "organizations/organization_form.html"
    fields = ["name", "city"]
    permission_required = "organizations.add_organization"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class OrganizationUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, UpdateView, PermissionRequiredMixin
):
    model = Organization
    template_name = "organizations/organization_form.html"
    fields = ["name", "city"]
    permission_required = "organizations.update_organization"

    def test_func(self):
        organization = self.get_object()
        return self.request.user == organization.owner


class OrganizationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Organization
    template_name = "organizations/delete_confirm.html"
    success_url = "/"
    permission_required = "organization.delete_organization"

    def test_func(self):
        organization = self.get_object()
        return self.request.user == organization.owner
