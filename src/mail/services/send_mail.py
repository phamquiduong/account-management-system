from django.conf import settings
from django.template.loader import render_to_string
from django.utils.module_loading import import_string

from mail.services.backend import SendMailBackend


class SendMailService:
    def __init__(
        self,
        to: list[str],
        subject: str,
        content: str,
        cc: list[str] | None = None,
        bcc: list[str] | None = None,
        email_backend: type[SendMailBackend] | None = None,
    ) -> None:
        self.to = to
        self.subject = subject
        self.content = content
        self.cc = cc
        self.bcc = bcc
        self.email_backend: type[SendMailBackend] = email_backend or import_string(settings.SEND_EMAIL_BACKEND)

    @staticmethod
    def render_content(template_name: str, **context) -> str:
        return render_to_string(template_name, context=context)

    def send(self):
        self.email_backend(to=self.to, subject=self.subject, content=self.content, cc=self.cc, bcc=self.bcc).send_html()
