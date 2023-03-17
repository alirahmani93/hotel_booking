import base64
import logging
import pathlib
from random import randint
from django.utils.translation import gettext_lazy as _

from django.core.cache import cache
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.conf import settings

from applications.common.statuses import *


def encode_base64(string):
    string = string
    string_bytes = string.encode("ascii")

    base64_bytes = base64.b64encode(string_bytes)
    base64_string = base64_bytes.decode("ascii")

    return base64_string


def decode_base64(payload):
    base64_string = f" {payload} =="
    base64_bytes = base64_string.encode("ascii")

    payload_bytes = base64.b64decode(base64_bytes)
    payload_decoded = payload_bytes.decode("ascii")

    return payload_decoded


def notify_by_email(recipient_list, template_name, subject, context, **kwargs):
    """
    Send an email to the provided recipient_list using the subject and the prepared template.

    Parameters:
    recipient_list (List): A Python list of emails
    template_name (String): Relative address of the template.
    subject (String): Subject of the email to be sent.
    context (Dict): The context which the template is filled with.
    **kwargs: Arbitrary keyword arguments which are considered as http request headers.


    Returns:
    int: Indicates email serivce's response. Either 1 or 0.
          ( 1 for success. 0 for failure.)
    """
    message = get_template(template_name).render(context)
    if kwargs:
        msg = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=recipient_list,
            headers=context
        )
    else:
        msg = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=recipient_list
        )

    msg.content_subtype = "html"
    response = msg.send()

    return response


def send_email(email, url: str = None):
    try:
        otp = str(randint(0, 99999)).zfill(5)
        cache.set(email, otp, 60 * 5)
        if not url:
            url = "/api/user/verify/email/"
        target_url = f'{settings.SITE_URL}{url}'
        url_appendix = str(otp) + ';' + str(email)  # otp;email"

        # notify_by_email(
        #     recipient_list=[email],
        #     template_name='common/enduser_mail.html',
        #     subject=_('email verification'),
        #     context={
        #         'otp_code': str(otp),
        #         'verification_url': target_url + f'?payload={encode_base64(url_appendix)}'})
        print(otp)
        return {'detail': _('OTP is sent to you')}, OK_200
    except Exception as e:
        logging.log(level=logging.CRITICAL, msg=f"some error in send email:{pathlib.Path.parent} {e.__str__()}")
        return {'detail': e.__str__()}, SERVER_ERROR_500
