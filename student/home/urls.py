from django.urls import path

from .views import index, about, send_message, DeleteView, error404, Add_Students
from .auth import Login, Signup, Logout

from django.contrib.auth import views as auth_views

from django.contrib.auth import views as auth_views

from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", index, name="index"),
    path('404', error404, name='404'),
    path('add', Add_Students.as_view() ,name='add_student'),
    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path("logout", Logout.as_view(), name="logout"),
    path("<slug:slug>", about, name="about"),
    path("send_message/<int:id>", send_message, name="send_message"),
    path('delete/<slug:slug>', DeleteView.as_view(), name='delete'),

    # path("password_reset", )
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='home/password_reset_form.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='home/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='home/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='home/password_reset_complete.html'), name='password_reset_complete'),
]
   
