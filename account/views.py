from django.shortcuts import redirect, render
from .forms import LoginForm, RegisterForm, ResetPasswordForm, ProfileForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

def login_view(request):
    if request.user.is_authenticated:
        return redirect('shelf:index')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(request.POST.get('next') or 'shelf:index')
    else:
        form = LoginForm(request)
    
    context = {
        "form": form,
        'next': request.GET.get('next', ''),
    }

    return render(request, 'account/login.html', context)

def register_view(request):
    if request.user.is_authenticated:
        return redirect('shelf:index')
    
    context = {}
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('shelf:index')
    else:
        form = RegisterForm()
        context['form'] = form
        
    return render(request, 'account/register.html', context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('shelf:index')

@login_required
def reset_password_view(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Keep the user logged in after their password changes
            update_session_auth_hash(request, user)
            messages.success(request, "Your password has been updated.")
            return redirect('account:profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ResetPasswordForm(request.user)

    return render(request, 'account/reset_password.html', {'form': form})

def reset_password_done_view(request):
    return render(request, 'account/reset_password_done.html')

@login_required
def profile_view(request):
    context = {
        'user': request.user,
    }
    return render(request, 'account/profile.html', context)


@login_required
def profile_edit_view(request):
    context = {}
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect('account:profile')
    else:
        context['form'] = ProfileForm(instance=request.user)

    return render(request, 'account/profile_edit.html', context)