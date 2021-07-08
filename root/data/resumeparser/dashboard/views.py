from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from .parser import Engine

en = Engine()


class Index(View):
    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        text = request.POST.get('text')
        return JsonResponse({
            'status':'OK',
            'result':en.tokeninzer(text)
        })