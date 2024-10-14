import random
import string

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import redirect
from django.utils import timezone
from formtools.wizard.views import SessionWizardView

from teachers.models import Creator
from users.forms import creator_forms as forms


# Create your views here.
class CreatorSignUpView(SessionWizardView):
    """
    This is the view for the sign up process for a Creator.
    """
    form_list = [
        ('email_details', forms.CreatorSignUpEmailForm),
        ('personal_details', forms.CreatorSignUpPersonalDetailForm),
        # ('creator_details', forms.CreatorSignUpCreatorDetailsForm),
        ('password_details', forms.CreatorSignUpPasswordForm)
    ]
    template_name = "users/creator_signup.html"

    def post(self, *args, **kwargs):
        current_step = self.steps.current
        form = self.get_form(data=self.request.POST, files=self.request.FILES)

        if current_step == 'email_details':
            email = self.request.POST.get('email_details-email')
            if email:
                existing_user = get_user_model().objects.filter(email=email).first()
                if existing_user:
                    if not existing_user.is_active or not existing_user.is_email_verified:
                        # User exists but not fully activated, send new OTP
                        otp = ''.join(random.choices(string.digits, k=6))
                        existing_user.otp = otp
                        existing_user.otp_created_at = timezone.now()
                        existing_user.save()
                        send_otp_email.delay(str(existing_user.id), otp)
                        messages.info(self.request,
                                      "An account with this email already exists. We've sent a new verification OTP.")
                        return redirect('accounts:verify_email_with_otp', user_id=existing_user.id)
                    else:
                        # User exists and is fully activated
                        messages.error(self.request,
                                       "An account with this email already exists. Please log in instead.")
                        return redirect('accounts:signin')

        return super().post(*args, **kwargs)

    def done(self, form_list, **kwargs):
        email_details = self.get_cleaned_data_for_step('email_details')
        personal_details = self.get_cleaned_data_for_step('personal_details')
        creator_details = self.get_cleaned_data_for_step('creator_details')
        password_details = self.get_cleaned_data_for_step('password_details')

        try:
            with transaction.atomic():
                user = get_user_model().objects.create_user(
                    email=email_details['email'],
                    username=email_details['username'],
                    full_name=personal_details['full_name'],
                    password=password_details['password1'],
                    is_active=True,
                    is_teacher=True,  # Set is_teacher to True for Creator accounts
                    is_email_verified=False,
                )
                creator = Creator.objects.create(
                    user=user,
                )
                user.save()
                creator.save()

                # Generating OTP
                otp = ''.join(random.choices(string.digits, k=6))
                user.otp = otp
                user.otp_created_at = timezone.now()
                user.save()
                send_otp_email.delay(str(user.id), otp)

        except Exception as e:
            messages.error(self.request, "An error occurred during signup. Please try again.")
            return self.render_revalidation_failure('personal_details', form_list, **kwargs)

        messages.success(self.request, "Your account has been created. Please verify your email with OTP sent.")
        return redirect('accounts:verify_email_with_otp', user_id=user.id)
