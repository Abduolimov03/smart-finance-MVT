from django.urls import path
from .views import signup_view, verify_view, login_view, home_view, forgot_password_view, reset_password_view, \
    logout_view, change_profile

urlpatterns = [
    path("", signup_view, name="signup"),
    path("verify/", verify_view, name="verify"),
    path("login/", login_view, name="login"),
    path("home/", home_view, name="home"),
    path("forgot-password/", forgot_password_view, name="forgot_password"),
    path("reset-password/", reset_password_view, name="reset_password"),
    path("logout/", logout_view, name="logout"),
    path("profile/", change_profile, name="change_profile"),

]
