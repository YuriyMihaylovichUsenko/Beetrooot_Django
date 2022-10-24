from django.core.mail import send_mail
from django.conf import settings
from django.template import loader


def send_email_func(
        subject,
        recipient_list,
        html_template,
        context,
        from_email=settings.DEFAULT_FROM_EMAIL,
        message=''
):
    html_message = loader.render_to_string(html_template, context)
    return send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipient_list,
                html_message=html_message
            )
