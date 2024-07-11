from django.urls import path

from interface.views import AddUserToOrganizationView, CreateOrganizationView, ObtainTokenPairView, OrganizationListView, RegisterView, RetrieveOrganisationView, UserDetailView, get_user_detail
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('login', ObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/<str:userId>/', UserDetailView.as_view(), name='user-detail'),
    path('organisations/<str:orgId>/', RetrieveOrganisationView.as_view(), name='org-detail'),
    path('organisations/', OrganizationListView.as_view(), name='organisation'),
    path('organisations/<uuid:orgId>/users', AddUserToOrganizationView.as_view(), name='add-user-to-organisation'),
    path('create-organisation/', CreateOrganizationView.as_view(), name='create-organisation'),
]
