from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("create/", views.create_event, name="create_event"),

    path("event/<int:event_id>/", views.event_detail, name="event_detail"),
    path("event/<int:event_id>/rsvp/", views.toggle_rsvp, name="toggle_rsvp"),
    path("update/<int:event_id>/", views.update_event, name="update_event"),
    path("delete/<int:event_id>/", views.delete_event, name="delete_event"),
]
