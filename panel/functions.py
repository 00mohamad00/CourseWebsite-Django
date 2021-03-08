import csv
from django.http import HttpResponse
from .models import Answer

def download_csv(objects):
    response = HttpResponse(content_type='text/csv')
    # force download.
    response['Content-Disposition'] = 'attachment;filename=export.csv'

    # the csv writer
    writer = csv.writer(response)
    writer.writerow(['شماره دانشجویی', 'نام و نام خانوادگی', 'تاریخ ارسال', 'نمره'])
    for obj in objects:
        writer.writerow([obj.student.student_id, obj.student.get_full_name(), str(obj.submitted_date), obj.score])

    return response