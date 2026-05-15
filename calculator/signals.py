from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils import timezone
from .models import UserSessionLog


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    role = "Manager" if user.is_staff else "Ordinary User"

    log = UserSessionLog.objects.create(
        user=user,
        login_time=timezone.now(),
        role=role
    )
    request.session['current_session_log_id'] = log.id


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    log_id = request.session.get('current_session_log_id')
    if log_id:
        try:
            log = UserSessionLog.objects.get(id=log_id)
            log.logout_time = timezone.now()
            log.duration = log.logout_time - log.login_time
            log.save()
        except UserSessionLog.DoesNotExist:
            pass
