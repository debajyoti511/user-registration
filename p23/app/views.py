from django.shortcuts import render
from .forms import *
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    un = request.session.get('username')
    if un:
        UO = User.objects.get(username=un)
        d = {'UO': UO}
        return render(request, 'home.html', d)
    return render(request, 'home.html')


def register(request):
    EUFO = UserForm()
    EPFO = ProfileForm()
    if request.method == 'POST' and request.FILES:
        UFDO = UserForm(request.POST)
        PFDO = ProfileForm(request.POST, request.FILES)
        if UFDO.is_valid() and PFDO.is_valid():
            pw = UFDO.cleaned_data.get('password')
            MUFDO = UFDO.save(commit=False)
            MUFDO.set_password(pw)
            MUFDO.save()
            MPFDO = PFDO.save(commit=False)
            MPFDO.username = MUFDO
            MPFDO.save()
            message = f"Hello {MUFDO.username}, \n Thank You For Registering to our website, with pno {MPFDO.pno}\n \n Thanks & regards \n \t Team"
            email = MUFDO.email
            send_mail(
                "Thanks For Registration",
                message,
                'debajyotin56@gmail.com',
                [email],
                fail_silently=False
            )
            return HttpResponseRedirect(reverse('user_login'))
            
    d = {'userform': EUFO, 'profileform': EPFO}
    return render(request, 'register.html', d)



def user_login(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        pw = request.POST.get('pw')
        AUO = authenticate(username=un, password=pw)
        if AUO and AUO.is_active:
            login(request, AUO)
            request.session['username'] = un
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('Invalid Cresdentials')
    return render(request, 'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))