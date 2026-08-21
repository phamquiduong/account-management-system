from abc import ABC, abstractmethod

from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from mail.models import Email


class SendMailBackend(ABC):
    def __init__(
        self, to: list[str], subject: str, content: str, cc: list[str] | None = None, bcc: list[str] | None = None
    ):
        self.to = to
        self.subject = subject
        self.content = content
        self.cc = cc
        self.bcc = bcc

    @abstractmethod
    def send_html(self): ...


class SMTPBackend(SendMailBackend):
    def __init__(
        self, to: list[str], subject: str, content: str, cc: list[str] | None = None, bcc: list[str] | None = None
    ):
        super().__init__(to, subject, content, cc, bcc)
        self._create_log()

    def send_html(self):
        self._set_log_status(Email.Status.SENDING)

        try:
            msg = EmailMultiAlternatives(
                to=self.to,
                cc=self.cc,
                bcc=self.bcc,
                subject=self.subject,
                body=self.content,
                from_email=settings.FROM_EMAIL,
            )
            msg.attach_alternative(self.content, "text/html")
            msg.send()
        except Exception as exc:
            self._set_log_exception(exc)
            raise

        self._set_log_status(Email.Status.SENT)

    def _create_log(self):
        self.email_log = Email.objects.create(
            to=", ".join(self.to),
            cc=", ".join(self.cc or []),
            bcc=", ".join(self.bcc or []),
            subject=self.subject,
            content=self.content,
        )

    def _set_log_status(self, status: Email.Status):
        self.email_log.status = status
        self.email_log.save(update_fields=["status"])

    def _set_log_exception(self, exc: Exception):
        self.email_log.status = Email.Status.FAILED
        self.email_log.exception = str(exc)
        self.email_log.save(update_fields=["status", "exception"])
