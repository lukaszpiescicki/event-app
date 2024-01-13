from django.urls import path
from . import views
from .views import OrganizationCreateView, OrganizationUpdateView, OrganizationDeleteView

urlpatterns = [
    path('organization/new/', OrganizationCreateView.as_view(), name='organization-create'),
    path('organization/update/<int:pk>', OrganizationUpdateView.as_view(), name='organization-update'),
    path('organization/delete/<int:pk>', OrganizationDeleteView.as_view(), name='organization-delete'),
]
