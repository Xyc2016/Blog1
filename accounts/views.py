from django.shortcuts import render

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import Http404


# Create your views here.


def log_in(request):
    if request.method == 'GET':
        return render(request, 'accounts/log_in.html')
    elif request.method == 'POST':
        user = authenticate(request, username=request.POST['username'],
                            password=request.POST['password'])
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('post:index'))
        else:
            return HttpResponseRedirect(reverse('accounts:login'))


def profile(request):
    if request.user.is_authenticated:
        return render(request, 'accounts/profile.html')
    else:
        raise Http404()


def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('post:index'))
