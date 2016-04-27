from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^about/$', TemplateView.as_view(template_name="core/about_us.html"), name='about'),
    url(r'^downloads/$', TemplateView.as_view(template_name="core/downloads.html"), name='downloads'),
]