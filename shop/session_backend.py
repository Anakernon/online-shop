from django.contrib.sessions.backends.db import SessionStore as mainSessionStore
from django.contrib.sessions.models import Session
from .settings import BASE_DIR
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(BASE_DIR), os.path.pardir)))
from menu.models import *
import copy

class SessionStore(mainSessionStore):
    def cycle_key(self):
        session = Session.objects.get(session_key=self.session_key)
        cartItemSet = copy.copy(CartItem.objects.filter(session = session))
        ret = mainSessionStore.cycle_key(self)
        session = Session.objects.get(session_key=self.session_key)
        
        if cartItemSet.count():
            for cartItem in cartItemSet:
                cartItem.session = session
                cartItem.save()

        cart = Cart(session = session, cost = 0, total_cost = 0)
        cart.save()
        cart = Cart.objects.get(session = session)
        cart.items.set(cartItemSet)
        cart.count_cost()
        cart.save()
            
        return ret
        
        
        
        
        
        
        
        
        
