import json
from dataclasses import dataclass
from base64 import b64encode
from io import BytesIO

import requests
from django.template import Template, Context
from celery import shared_task
from django.core.files import File

from restaurant_api.models import Check, CheckStatus


@dataclass
class Item:
    name: str
    quantity: int


class Order:
    def __init__(self, id: int, data: dict):
        self.id = id
        self.data = [
            Item(name=key, quantity=value) for key, value in data.items()
        ]


@shared_task
def make_check_pdf(
        check_id: int,
        order: dict,
        check_type: str,
        template_name: str,
        point_id: int,
) -> None:
    order = Order(**order)
    html = render_template(obj=order, template_name=template_name)
    pdf = make_pdf(html_file=html)
    pdf_name = f"{order.id}_{check_type}_point{point_id}.pdf"

    check = Check.objects.get(id=check_id)
    check.status = CheckStatus.RENDERED
    check.pdf_file = File(BytesIO(pdf), pdf_name)
    check.save()


def render_template(obj, template_name: str) -> bytes:
    with open(template_name, "r") as f:
        template = Template(f.read())
    html_file = template.render(context=Context({"obj": obj}))
    return bytes(str(html_file), encoding="utf8")


def make_pdf(html_file: bytes) -> bytes:
    url = 'http://htmltopdf:80/'
    encoding = "utf-8"

    base64_bytes = b64encode(html_file)
    base64_string = base64_bytes.decode(encoding)

    data = {"contents": base64_string}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response.content
