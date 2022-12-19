from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from restaurant_api.crud import (
    create_checks,
    get_printers_by_point_id,
    get_checks,
    print_checks,
)
from restaurant_api.models import CheckType, CheckStatus
from restaurant_api.serializers import OrderSerializer


@csrf_exempt
def place_order(request):
    if request.method != "POST":
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    order_data = JSONParser().parse(request)
    serializer = OrderSerializer(data=order_data)

    if not serializer.is_valid():
        return JsonResponse(
            {"error": "Order data is incorrect"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    point_id = order_data.get("point_id")
    printers = get_printers_by_point_id(point_id=point_id)
    if not printers:
        return JsonResponse(
            {"error": "There are no printers for the provided point"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    order_id = order_data.get("order_id")
    created_checks = get_checks(point_id=point_id, order_id=order_id)
    if created_checks:
        return JsonResponse(
            {"detail": "Provided order is already created"},
            status=status.HTTP_200_OK,
        )

    order = {"id": order_id, "data": order_data.get("data")}
    create_checks(order=order, point_id=point_id)
    return JsonResponse(
        {"order_id": order_id},
        status=status.HTTP_201_CREATED,
    )


@csrf_exempt
def print_checks(request, printer_api_key: str):
    if request.method != "POST":
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    unprinted_checks = get_checks(
        printer_api_key=printer_api_key,
        check_status=CheckStatus.RENDERED,
    )
    if not unprinted_checks:
        return JsonResponse(
            {"detail": "There are no unprinted checks for provided printer"},
            status=status.HTTP_200_OK,
        )

    checks_pdf = [check.pdf_file.url for check in unprinted_checks]
    print_checks(checks=unprinted_checks)

    return JsonResponse(
        checks_pdf,
        status=status.HTTP_201_CREATED,
        safe=False,
    )
