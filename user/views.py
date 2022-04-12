from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from tool import ret_code


class AddUser(View):
    def get(self):
        return JsonResponse(ret_code(200))
