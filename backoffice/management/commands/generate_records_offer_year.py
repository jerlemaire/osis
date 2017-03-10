
from base import models as mdl_base


def create_offer_year(offer,academic_year,structure_sector,structure_fac,structure_pgm,acronym,title,title_short,grade,
                       recipient,location, postal_code,city, country,campus):
    offer_year = mdl_base.offer_year.OfferYear.objects.create(offer=offer, academic_year=academic_year,
                                                              entity_administration=structure_sector,
                                                              entity_administration_fac=structure_fac,
                                                              entity_management=structure_pgm,
                                                              acronym=acronym,
                                                              title=title,
                                                              title_short=title_short,
                                                              grade=grade, recipient=recipient,
                                                              location=location,
                                                              postal_code= postal_code,
                                                              city=city, country=country,campus=campus)
    return offer_year