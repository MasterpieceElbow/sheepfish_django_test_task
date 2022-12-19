from typing import Optional
import os

from django.db.models.query import QuerySet

from restaurant_api.models import (
    Check,
    Printer,
    CheckType,
    CheckStatus,
)

from restaurant_api.tasks import make_check_pdf


TEMPLATE_DIR = "templates"
CHECK_TYPE_TEMPLATES = {
    CheckType.CLIENT: "client_check.html",
    CheckType.KITCHEN: "kitchen_check.html",
}


def get_last_order_id() -> Optional[int]:
    last_check = Check.objects.order_by("id").last()
    if not last_check:
        return

    check_data = last_check.order
    return check_data["id"]


def create_checks(order: dict, point_id: int) -> None:
    point_printers = get_printers_by_point_id(point_id=point_id)

    for printer in point_printers:
        check = Check(
            printer=printer,
            type=printer.check_type,
            order=order,
        )
        check.save()

        template_path = (os.path.join(
            TEMPLATE_DIR, CHECK_TYPE_TEMPLATES[printer.check_type]
        ))

        make_check_pdf.delay(
            check_id=check.id,
            check_type=check.type,
            order=check.order,
            template_name=template_path,
            point_id=point_id,
        )


def get_printers_by_point_id(point_id: int, check_type=None):
    queryset = Printer.objects.filter(point_id=point_id)
    if check_type:
        queryset = queryset.filter(check_type=check_type)
    return queryset


def get_checks(
        point_id: int = None,
        order_id: int = None,
        check_status: str = None,
        printer_api_key: str = None,
):
    queryset = Check.objects.all()
    if printer_api_key:
        queryset = queryset.filter(printer__api_key=printer_api_key)
    if point_id:
        queryset = queryset.filter(printer__point_id=point_id)
    if order_id:
        queryset = queryset.filter(order__id=order_id)
    if check_status:
        queryset = queryset.filter(status=check_status)
    return queryset


def print_checks(checks: QuerySet[Check]) -> None:
    checks.update(status=CheckStatus.PRINTED)
