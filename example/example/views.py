from django.shortcuts import render
from django.views.generic import View

from steps import Process, Step


def view1(request):
    return render(request, 'view.html', {})


def view2(request):
    return render(request, 'view.html', {})


def view3(request):
    return render(request, 'view.html', {})


def view4(request):
    return render(request, 'view.html', {})


class View5(View):
    def get(self, request):
        return render(request, 'view.html', {})


class MyProcess(Process):
    views = [
        view1,
        Step(view2, 'view2', 'Step 2', r'^something/$'),
        (view3, 'view3', 'Step 3', r'^something-else/$'),
        view4,
        (View5.as_view(), 'view5'),
    ]


class MyProcess2(Process):
    views = [
        (View5.as_view(), 'view5'),
        view2,
        view4,
        (view3, 'view3', 'Step 3', r'^whatever/$'),
    ]
