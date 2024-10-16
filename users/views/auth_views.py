import random
import string
from urllib.parse import urlparse, parse_qs

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import FormView, TemplateView

from users.forms.auth_forms import LoginForm
from users.forms.forms import ChangePasswordForm, UserAccountUpdateForm
from users.tasks.task_send_otp import send_otp_email


class LoginView(View):
    template_name = 'users/login.html'
    form_class = LoginForm

    def get(self, request):
        if request.user.is_authenticated and request.user.is_teacher:
            messages.info(self.request, 'You are already logged in.')
            return redirect('teachers:creator_dashboard')
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
                        if request.user.is_teacher:
                            return redirect('teachers:creator_dashboard')
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


@method_decorator([login_required], name='dispatch')
class UserAccountUpdateView(FormView):
    """
    This view updates the user account records
    It updates the user password and the user details
    """
    template_name = 'users/update_user_account.html'

    # success_url = reverse_lazy('customers:customer_dashboard')

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        user = get_user_model().objects.get(id=user_id)
        user_form = UserAccountUpdateForm(instance=user)
        password_form = ChangePasswordForm(user)
        return render(request, self.template_name, {
            'user_form': user_form,
            'password_form': password_form
        })

    def post(self, request, *args, **kwargs):
        if request.POST.get('action') == 'update_user_details':
            user_form = UserAccountUpdateForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                if request.user.is_teacher:
                    messages.success(request, 'Your profile has been updated')
                    return redirect(reverse('teachers:creator_dashboard'))
                else:
                    messages.success(request, 'Your profile has been updated')
                    return redirect(reverse('teachers:creator_dashboard'))

        elif request.POST.get('action') == 'update_user_password':
            password_form = ChangePasswordForm(request.user, request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)
                if request.user.is_teacher:
                    messages.success(request, 'Your profile has been updated')
                    return redirect(reverse('teachers:creator_dashboard'))
                else:
                    messages.success(request, 'Your profile has been updated')
                    return redirect(reverse('teachers:creator_dashboard'))


class SignUpView(TemplateView):
    """
    This is the signup landing page view
    """
    template_name = 'users/signup.html'
