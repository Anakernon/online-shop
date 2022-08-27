from django.http import HttpResponseRedirect, HttpResponse
import stripe
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname("Documents/online-shop"), os.path.pardir)))

import stripe_keys
import menu.models as menu_db
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from .models import *

stripe.api_key = stripe_keys.SECRET_KEY

@login_required(login_url = "/login")
def submit(request):
    session = Session.objects.get(session_key=request.session.session_key)
    
    if not menu_db.Cart.objects.filter(session = session).count():     
        cart = menu_db.Cart(session = session, cost = 0, total_cost = 0)
        cart.save()
           
    cartdata = menu_db.Cart.objects.get(session = session)
    items = menu_db.CartItem.objects.filter(session = session)
    cartdata.items.set(items)
    cartdata.count_cost()
    cartdata.save()
    
    product_names = ""
    product_prices = ""
    product_quantities = ""
    
    for cartitem in cartdata.items.all():
        product_names = product_names + cartitem.product.name + ". "
        product_prices = product_prices + str(cartitem.total_cost()) + " "
        product_quantities = product_quantities + str(cartitem.quantity) + ". "
    
    potential_order = b4Q(
                                            user_name = request.user.username,
                                            user_id = request.user.id,
                                            user_phone = request.user.extensions.phone,
                                            user_email = request.user.email,
                                            user_address = request.user.extensions.address,
                                            cart_id = cartdata.id,
                                            product_names = product_names,
                                            product_prices = product_prices,
                                            product_quantities = product_quantities,
                                            paid_amount = cartdata.total_cost
    )
    potential_order.save()
    
    for item in cartdata.items.all():
        item.delete()
    cartdata.delete()
    
    checkout_session = stripe.checkout.Session.create(
        payment_method_types = ["card"],
        line_items=[{
                              'price_data': {
                                'currency': 'usd',
                                'product_data': {
                                  'name': f"{potential_order.cart_id}",
                                },
                                'unit_amount': potential_order.paid_amount, 
                              },
                              'quantity': 1,
        }],
        metadata = {"order_id" : potential_order.cart_id},
        mode = "payment",
        success_url = stripe_keys.DOMAIN + "/profile/",
        cancel_url = stripe_keys.DOMAIN + "/cart/", 
    )
    return HttpResponseRedirect(checkout_session.url)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, stripe_keys.WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        customer_email = session["customer_detail"]["email"]
        order_id = session["meatadata"]["order_id"]
        
        order = b4Q.objects.get(cart_id = order_id)
        new_order = OrderInQueue(
                                                        user_name = order.user_name,
                                                        user_id = order.user_id,
                                                        user_phone = order.user_phone,
                                                        user_email = order.user_email,
                                                        user_address = order.user_address,
                                                        cart_id = order.cart_id,
                                                        product_names = order.product_names,
                                                        product_prices = order.product_prices,
                                                        product_quantities = order.product_quantities,
                                                        paid_amount = order.paid_amount
        )
        new_order.save()
        order.delete()
        
        message = ""
        names = new_order.product_names.split(". ")
        prices = new_order.product_prices.split(" ")
        quantities = new_order.product_quantities.split(". ")
        for i, _ in enumerate(names):
            message = message + names[i] + "  " + prices[i] + "  x" + quantities[i] + "\n"
        
        send_mail(
                            subject = f"Order for {new_order.cart_id}",
                            message = message,
                            recipient_list = [customer_email, stripe_keys.SHOP_EMAIL],
                            from_email = stripe_keys.SHOP_EMAIL
        )
    
    return HttpResponse(status = 200)















