import enum

from django.db import models


class CheckType(str, enum.Enum):
    KITCHEN = "kitchen"
    CLIENT = "client"


class CheckStatus(str, enum.Enum):
    NEW = "new"
    RENDERED = "rendered"
    PRINTED = "printed"


CHECK_TYPE_CHOICES = [
    (CheckType.KITCHEN.value, "kitchen"),
    (CheckType.CLIENT.value, "client"),
]


CHECK_STATUS_CHOICES = [
    (CheckStatus.NEW.value, "new"),
    (CheckStatus.RENDERED.value, "rendered"),
    (CheckStatus.PRINTED.value, "printed"),
]


class Printer(models.Model):
    name = models.CharField(max_length=60)
    api_key = models.CharField(max_length=60, unique=True, blank=True)
    check_type = models.CharField(max_length=60, choices=CHECK_TYPE_CHOICES)
    point_id = models.IntegerField()

    # api_key is unique and consists of check_type and point_id
    def save(self, *args, **kwargs):
        self.api_key = f"{self.point_id}_{self.check_type}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.api_key

    class Meta:
        unique_together = ("check_type", "point_id")


class Check(models.Model):
    printer = models.ForeignKey(Printer, on_delete=models.DO_NOTHING)
    type = models.CharField(max_length=60, choices=CHECK_TYPE_CHOICES)
    order = models.JSONField()
    status = models.CharField(
        max_length=60,
        choices=CHECK_STATUS_CHOICES,
        default="new"
    )
    pdf_file = models.FileField(
        upload_to="pdf/",
        null=True,
        blank=True,
    )

    def __str__(self):
        order_id = self.order.get("id")
        return f"OrderId_{order_id}_type_{self.type}"

    class Meta:
        ordering = ["id"]
