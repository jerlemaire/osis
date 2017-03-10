from base import models as mdl_base
import datetime
from datetime import date


def create_academic_calendar_year(academic_year,start_date, end_date,event):
    today = date.today()
    academic_calendar_year =None
    if (today.month > 9 or today.month <= 2):
        academic_calendar_year= mdl_base.academic_calendar.AcademicCalendar(
            academic_year=academic_year, start_date=start_date,
            end_date=end_date, title="%s%d" % (event, 1))
    elif (today.month >= 3 and today.month < 7):
        academic_calendar_year = mdl_base.academic_calendar.AcademicCalendar(
            academic_year=academic_year, start_date=start_date,
            end_date=end_date, title="%s%d" % (event, 2))

    else:
        academic_calendar_year = mdl_base.academic_calendar.AcademicCalendar(
                academic_year=academic_year, start_date=start_date,
                end_date=end_date, title="%s%d" % (event, 3))

    return academic_calendar_year

#encoding date : now > end_date
def create_academic_calendar_encoding_event_in_past(academic_year):
    encoding_event = 'Encodage de notes session'
    today = date.today()
    start_date=datetime.datetime(today.year, today.month, today.day-15)
    end_date=datetime.datetime(today.year, today.month, today.day-1)
    return  create_academic_calendar_year(academic_year,start_date, end_date,encoding_event)


    # encoding date : start_date <=now <= end_date
def create_academic_calendar_encoding_event_in(academic_year):
    encoding_event = 'Encodage de notes session'
    today = date.today()
    start_date = datetime.datetime(today.year, today.month, today.day)
    end_date = datetime.datetime(today.year, today.month, today.day+15)
    return  create_academic_calendar_year(academic_year,start_date, end_date,encoding_event)

    # encoding date : end_date < now
def create_academic_calendar_encoding_event_in_fiture(academic_year):
        encoding_event = 'Encodage de notes session'
        today = date.today()
        start_date = datetime.datetime(today.year, today.month, today.day + 1)
        end_date = datetime.datetime(today.year, today.month, today.day + 15)
        return create_academic_calendar_year(academic_year,start_date, end_date,encoding_event)

        # delibe date :  start_date <=now <= end_date
def create_academic_calendar_delibe_event_in(academic_year):
    encoding_event = 'Deliberation session'
    today = date.today()
    delibe_date = datetime.datetime(today.year, today.month, today.day)
    return create_academic_calendar_year(academic_year,delibe_date, delibe_date, encoding_event)


    # delibe date :  start_date <=now <= end_date
def create_academic_calendar_delibe_event_in_fiture(academic_year):
    encoding_event = 'Deliberation session'
    today = date.today()
    delibe_date = datetime.datetime(today.year, today.month, today.day+1)
    return create_academic_calendar_year(academic_year, delibe_date, delibe_date, encoding_event)

