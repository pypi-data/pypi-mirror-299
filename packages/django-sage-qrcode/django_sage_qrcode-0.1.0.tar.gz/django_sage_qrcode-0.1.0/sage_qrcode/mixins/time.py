from django.db import models
from django.utils.translation import gettext_lazy as _


class TimestampMixin(models.Model):
    """"""

    created = models.DateTimeField(
        _("Created"),
        auto_now_add=True,
        help_text=_("Date and time of record creation"),
    )

    modified = models.DateTimeField(
        _("Modified"),
        auto_now=True,
        help_text=_("Date and time of record modification"),
    )

    class Meta:
        abstract = True
