from base import models as mdl_base
import datetime
from datetime import date



def create_academic_year(start_date, end_date):
    year = start_date.year
    academic_year = mdl_base.academic_year.AcademicYear.objects.create(year=year, start_date= start_date,
                                                                       end_date=end_date)
    return academic_year


def create_academic_year_in_past():
    today = date.today()
    start_date =None
    end_date=None
    if ( today.month > 9 or ( today.month == 9 and  today.day >= 15)):
        start_date= datetime.datetime(today.year-1, 9, 15)
        end_date = datetime.datetime(today.year, 9, 14)
    else :
        start_date= datetime.datetime(today.year-2, 9, 15)
        end_date=datetime.datetime(today.year-1, 9, 14)
    return create_academic_year(start_date, end_date)

def create_academic_year_actual():
    today = date.today()
    start_date = None
    end_date = None
    if ( today.month > 9 or ( today.month == 9 and  today.day >= 15)):
        start_date= datetime.datetime(today.year, 9, 15)
        end_date = datetime.datetime(today.year+1, 9, 14)
    else :
        start_date= datetime.datetime(today.year-1, 9, 15)
        end_date=datetime.datetime(today.year, 9, 14)

    return create_academic_year(start_date, end_date)


def create_academic_year_in_future():
    today = date.today()
    return create_academic_year(datetime.datetime(today.year+1, 9, 15), datetime.datetime(today.year+2, 9, 14))