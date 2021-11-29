from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views


# app_name = 'api'

urlpatterns = [
    # path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('logout/', views.BlacklistRefreshView.as_view(), name="logout"),
    # path('clients/', views.Clients.as_view(), name="clients"),
    # path('clients/<int:client_id>', views.Clients.as_view(), name="client_details"),
    ]
