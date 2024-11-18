from django.urls import path

from .views import index, about, send_message, DeleteView, error404, Add_Students


urlpatterns = [
    path("", index, name="index"),
    path('404', error404, name='404'),
    path('add', Add_Students.as_view() ,name='add_student'),
    path("<slug:slug>", about, name="about"),
    path("send_message/<int:id>", send_message, name="send_message"),
    path('delete/<slug:slug>', DeleteView.as_view(), name='delete'),
]
   
