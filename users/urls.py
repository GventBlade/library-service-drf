from django.urls import path
from users.views import CreateUserView, MangeUsersView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', CreateUserView.as_view(), name="register"),
    path('me/', MangeUsersView.as_view(), name="manage-profile"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

app_name = 'users'
