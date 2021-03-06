from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import Group
from django.core.cache import cache
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.template.defaultfilters import urlencode
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from django.views import generic

from osmaxx.contrib.auth.frontend_permissions import LoginRequiredMixin
from osmaxx.profile.forms import ProfileForm
from osmaxx.profile.models import Profile


class SendVerificationEmailMixin(object):
    RATE_LIMIT_SECONDS = 30

    def _send_email_verification(self, profile):
        if cache.get(profile.associated_user.id):
            return
        to_email = profile.unverified_email
        if to_email:
            cache.set(profile.associated_user.id, 'dummy value', timeout=self.RATE_LIMIT_SECONDS)
            user_administrator_email = settings.OSMAXX['ACCOUNT_MANAGER_EMAIL']
            token = profile.activation_key()
            token_url = '{}?token={}'.format(
                self.request.build_absolute_uri(reverse('profile:activation')), urlencode(token)
            )
            subject = render_to_string('profile/verification_email/subject.txt', context={}).strip()
            subject = ''.join(subject.splitlines())
            message = render_to_string(
                'profile/verification_email/body.txt',
                context=dict(
                    token_url=token_url,
                    username=self.request.user.username,
                    new_email_address=to_email,
                    domain=self.request.get_host(),
                )
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=user_administrator_email,
                recipient_list=[to_email],
            )
            messages.add_message(
                self.request, messages.INFO, _('To activate your email, click the link in the confirmation email.')
            )


class ProfileView(SendVerificationEmailMixin, LoginRequiredMixin, generic.UpdateView):
    form_class = ProfileForm
    template_name = 'profile/profile_edit.html'

    def get(self, *args, **kwargs):
        profile = self.get_object()
        user = self.request.user
        if not (user.email or user.profile.unverified_email):
            messages.add_message(
                self.request,
                messages.WARNING,
                _('You have not set an email address. You must set a valid email address to use OSMaxx.')
            )
        if self.is_new_user():
            self._move_email_from_user_to_profile(user, profile)
            self._send_email_verification(profile)
        else:
            self._ensure_profile_has_email(profile, user)
        user.refresh_from_db()
        return super().get(*args, **kwargs)

    def is_new_user(self):
        user = self.request.user
        profile_is_new = user.profile.unverified_email is None
        user_has_already_access = user_in_frontend_group(user)
        return profile_is_new and not user_has_already_access

    def post(self, *args, **kwargs):
        response = super().post(*args, **kwargs)
        if isinstance(response, HttpResponseRedirect):  # successful form validation
            profile = Profile.objects.get(associated_user=self.request.user)
            if profile.associated_user.email != profile.unverified_email:
                self._send_email_verification(profile=profile)
        return response

    def _ensure_profile_has_email(self, profile, user):
        if not profile.unverified_email:
            profile.unverified_email = user.email
            profile.save()

    def _move_email_from_user_to_profile(self, user, profile):
        if user.email:
            profile.unverified_email = user.email
            profile.save()
            user.email = ''
            user.save()

    def get_object(self, queryset=None):
        profile, _ = Profile.objects.get_or_create(associated_user=self.request.user)
        return profile

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, _('Profile successfully updated'))
        return reverse('profile:edit_view')


class ActivationView(SendVerificationEmailMixin, LoginRequiredMixin, generic.UpdateView):
    error_msg = _('Verification token too old or invalid. Please resend the confirmation email and try again.')

    def get(self, request, *args, **kwargs):
        user = request.user
        token = request.GET.get('token', None)
        if token:
            data = user.profile.validate_key(activation_key=token)
            if data:
                user.email = data['email']
                user.save()
                self._set_group(user)
                messages.add_message(self.request, messages.SUCCESS, _('Successfully verified your email address.'))
            else:
                messages.add_message(self.request, messages.ERROR, self.error_msg)
        else:
            messages.add_message(self.request, messages.ERROR, self.error_msg)
        return redirect(reverse('profile:edit_view'))

    def _set_group(self, user):
        if settings.REGISTRATION_OPEN and not user_in_frontend_group(user):
            self._grant_user_access(user)

    def _grant_user_access(self, user):
        group = Group.objects.get(name=settings.OSMAXX_FRONTEND_USER_GROUP)
        group.user_set.add(user)


class ResendVerificationEmail(SendVerificationEmailMixin, LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('profile:edit_view')

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(associated_user=self.request.user)
        self._send_email_verification(profile=profile)
        return super().get(request, *args, **kwargs)


def user_in_frontend_group(user):
    return user.groups.filter(name=settings.OSMAXX_FRONTEND_USER_GROUP).exists()
