from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .api.views import OrganizationModelViewSet
from .views import (
    OrganizationCreateView,
    OrganizationDeleteView,
    OrganizationsDetailView,
    OrganizationsListView,
    OrganizationUpdateView,
)

router = SimpleRouter()
router.register(r"organizations", OrganizationModelViewSet, basename="organizations")

urlpatterns = [
    path("organizations/", OrganizationsListView.as_view(), name="organizations-home"),
    path(
        "organizations/<int:pk>/",
        OrganizationsDetailView.as_view(),
        name="organization-detail",
    ),
    path(
        "organization/new/",
        OrganizationCreateView.as_view(),
        name="organization-create",
    ),
    path(
        "organization/update/<int:pk>",
        OrganizationUpdateView.as_view(),
        name="organization-update",
    ),
    path(
        "organization/delete/<int:pk>",
        OrganizationDeleteView.as_view(),
        name="organization-delete",
    ),
    path("api/v1/", include(router.urls)),
]
