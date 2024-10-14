import random
import string
from urllib.parse import urlparse, parse_qs

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View

from users.forms.auth_forms import LoginForm


class LoginView(View):
    template_name = 'accounts/public/login.html'
    form_class = LoginForm

    def get(self, request):
        if request.user.is_authenticated:
            messages.info(self.request, 'You are already logged in.')
            return redirect('core:public_dashboard')
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    if user.is_email_verified:
                        login(request, user)
                        messages.success(request, "Login successful")

                        # Handle 'next' parameter
                        next_page = request.GET.get('next')
                        if not next_page:
                            url = request.META.get('HTTP_REFERER', '')
                            parsed_url = urlparse(url)
                            params = parse_qs(parsed_url.query)
                            next_page = params.get('next', [None])[0]

                        if next_page:
                            return redirect(next_page)
                        return redirect('core:dashboard')
                    else:
                        otp = ''.join(random.choices(string.digits, k=6))
                        user.otp = otp
                        user.otp_created_at = timezone.now()
                        user.save()
                        send_otp_email.delay(str(user.id), otp)
                        messages.error(request, "Your email is not verified. Please verify your email")
                        return redirect('users:send_otp', user_id=user.id)
                else:
                    messages.error(request, "Your account is not active. Please contact support.")
            else:
                messages.error(request, "Invalid email or password.")
        return render(request, self.template_name, context={'form': form})


class LogOutView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        logout(request)
        messages.success(request, "You have been successfully logged out.")
        return redirect('core:index')
