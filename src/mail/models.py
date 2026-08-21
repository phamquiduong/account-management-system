from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models.timestamp import TimestampModelMixin
from common.models.uuid import UUIDModelMixin


class Email(UUIDModelMixin, TimestampModelMixin):
    class Type(models.TextChoices):
        HTML = "HTML", _("HTML")
        Text = "Text", _("Text")

    class Status(models.TextChoices):
        PENDING = "PENDING", _("Pending")
        SENDING = "SENDING", _("Sending")
        SENT = "SENT", _("Sent")
        FAILED = "FAILED", _("Failed")

    to = models.CharField(max_length=255)
    cc = models.CharField(max_length=255, blank=True, null=True)
    bcc = models.CharField(max_length=255, blank=True, null=True)

    subject = models.CharField(_("Subject"), max_length=1024)
    content = models.TextField(_("Content"))

    type = models.CharField(_("Type"), max_length=4, choices=Type, default=Type.HTML)

    status = models.CharField(_("Status"), max_length=7, choices=Status, default=Status.PENDING)

    exception = models.TextField(_("Exception"), blank=True, null=True)
