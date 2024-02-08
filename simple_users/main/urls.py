from django.urls import path
from .views import index, RegisterView, UsersLoginView, UsersLogoutView, PasswordEditView, ProfileEditView, profile, \
    user_activate, RegisterDoneView, PassResetView, PassResetConfirmView, user_detail

app_name = 'main'
urlpatterns = [
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('accounts/activate/<str:sign>/', user_activate, name='activate'),
    path('accounts/login/', UsersLoginView.as_view(), name='login'),
    path('accounts/password/edit/', PasswordEditView.as_view(), name='password_edit'),
    path('account/password/reset/', PassResetView.as_view(), name='password_reset'),
    path('accounts/password/reset/confirm/<uidb64>/<token>/', PassResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('accounts/profile/delete/', ProfileDeleteView.as_view(), name='profile_delete'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/profile/edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('accounts/logout/', UsersLogoutView.as_view(), name='logout'),
    path('users/<str:username>/', user_detail, name='user_detail'),
    path('', index, name='index')
]