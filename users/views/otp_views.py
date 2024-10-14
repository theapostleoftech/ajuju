import random
import string

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import View


class OTPVerificationView(View):
    template_name = 'accounts/public/otp_verification.html'

    def dispatch(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        user = get_user_model().objects.get(id=user_id)

        if user.is_email_verified:
            messages.info(request, "Your email is already verified. Please log in.")
            return redirect('accounts:public_signin')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, user_id):
        form = forms.OTPVerificationForm()
        return render(request, self.template_name, {'form': form, 'user_id': user_id})

    def post(self, request, user_id):
        form = forms.OTPVerificationForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            user = get_user_model().objects.get(id=user_id)
            if user.otp == otp and (timezone.now() - user.otp_created_at).total_seconds() < 600:
                user.is_email_verified = True
                user.otp = None
                user.otp_created_at = None
                user.save()

                # Send welcome email
                send_welcome_email.delay(str(user.id))

                messages.success(request, "Your email has been verified. You can log in now.")
                return redirect('accounts:public_signin')
            else:
                messages.error(request, "Invalid or expired OTP. Please try again or request a new OTP")
        return render(request, self.template_name, {'form': form, 'user_id': user_id})

class ResendOTPView(View):
    def get(self, request, user_id):
        user = get_user_model().objects.get(id=user_id)
        otp = ''.join(random.choices(string.digits, k=6))
        user.otp = otp
        user.otp_created_at = timezone.now()
        user.save()
        send_otp_email.delay(str(user.id), otp)
        messages.success(request, "A new OTP has been sent to your email.")
        return redirect('accounts:verify_email_with_otp', user_id=user.id)