from django.core.mail import send_mail
from core.meetings.models import Attendance
from Nexus import settings

from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_meeting_notification_by_email(attendance: Attendance):

    context = {
        "name": attendance.worker.get_fullname(),
        "link": attendance.meeting.link,
        "date": attendance.meeting.get_natural_date(),
        "organizer": attendance.meeting.organizer.get_fullname(),
        "field" : attendance.meeting.organizer.field.name,
        "position":attendance.meeting.organizer.position.name
    }

    html_message = render_to_string("email.html", context=context)
    plain_message = strip_tags(html_message)
    subject = f"Reunión {attendance.meeting.name} - {attendance.meeting.get_natural_date()}"
    to = attendance.worker.email

    send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [to], html_message=html_message)

