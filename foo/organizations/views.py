from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DeleteView, UpdateView

from .models import Organization


class OrganizationCreateView(LoginRequiredMixin, CreateView):
    model = Organization
    template_name = "organizations/organization_form.html"
    fields = ["name", "city"]


class OrganizationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Organization
    template_name = "organizations/organization_form.html"
    fields = ["name", "city"]
    permission_required = ...

    def test_func(self):
        organization = self.get_object()
        return 0  # TODO sprawdzić czy user jest w organizacji


class OrganizationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Organization
    template_name = "organizations/delete_confirm.html"
    success_url = "/"

    def test_func(self):
        organization = self.get_object()
        return 0  # TODO sprawdzić czy user utworzyl dana organizacje
