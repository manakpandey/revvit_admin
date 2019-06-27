from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^approved$', views.approved, name='approved'),
    url(r'^rejected$', views.rejected, name='rejected'),
    url(r'^logout$', views.sign_out, name='sign_out')
]
