from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import  UserPassesTestMixin

# Create your views here.




class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff



class IndexAdminView(TemplateView, AdminRequiredMixin):
    template_name = "Admin/indexAdmin.html"



