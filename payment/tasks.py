from io import BytesIO
from celery import shared_task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order

@shared_task
def payment_completed(order_id):
    """ Task to send an e-mail notification when an order is successfully created"""
    print("inside the send mail task celery")

    order=Order.objects.get(id=order_id)
    subject=f'My Shop - EE Invoice No {order.id}'
    message='please find attached the invoice for your recent purchase.'
    email=EmailMessage(subject,message,'ganapathy@testpress.in',[order.email])
    html=render_to_string('orders/order/pdf.html',{'order':order})
    out=BytesIO()
    stylesheets=[weasyprint.CSS(settings.STATIC_ROOT+'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out,stylesheets=stylesheets)
    email.attach(f'order_{order.id}.pdf',out.getvalue(),'application/pdf')

    email.send()