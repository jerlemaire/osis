
from base import models as mdl_base



def create_offer(title):
    offer = mdl_base.offer.Offer.objects.create(title=title)
    return offer
