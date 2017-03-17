
from base import models as mdl_base
import datetime

one_day = datetime.timedelta(days=1)
two_weeks = datetime.timedelta(days=15)

def create_offer_year_calendar(offer_year, academic_calendar, start_date, end_date):
    an_start_date = start_date if start_date !=None and start_date else academic_calendar.start_date

    an_end_date = end_date if end_date !=None else academic_calendar.end_date
    offer_year_calendar = mdl_base.offer_year_calendar.OfferYearCalendar.objects.create(offer_year=offer_year,
                                              academic_calendar=academic_calendar,
                                              start_date=an_start_date,
                                              end_date=an_end_date
                                              )
    return offer_year_calendar

def create_offer_year_calendar_in_past(offer_year,academic_year_calendar):
    start_date=academic_year_calendar.start_date - two_weeks
    end_date= academic_year_calendar.start_date - one_day
    return  create_offer_year_calendar(offer_year,academic_year_calendar,start_date, end_date)


def create_offer_year_calendar_in_fiture(offer_year,academic_year_calendar):
    start_date = academic_year_calendar.end_date +one_day
    end_date = academic_year_calendar.end_date + two_weeks
    return create_offer_year_calendar(offer_year, academic_year_calendar, start_date, end_date)



