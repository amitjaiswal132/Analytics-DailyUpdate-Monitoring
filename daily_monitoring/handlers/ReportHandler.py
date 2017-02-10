import logging
from analytics_common.handlers.email_handler import EmailHandler
from daily_monitoring.settings import *

class ReportHandler:
    logger = logging.getLogger(__name__)

    def __init__(self, date_str, hour):
        self.date_str = date_str
        self.hour = hour
        self.fail_msgs = []
        self.success_msgs = []
        self.body_prepend = ""
        self.body_append = ""
        self.enabled = True

def _generate_title(date_str, hour):
        title_format = "v2:Redshift Upload %s %s-%s "
        title = (title_format % (ENV_PREFIX, date_str, str(hour)))
        return title


def _generate_title(self, title_append):
    # v2:Daily Redshift Upload 2015-10-18 Start:8:00 AM Consumed: 150 m [Total:21 Waiting:2 Running:2 Success:17 Fail:0]
    title_format = "v2:%s Redshift Upload %s %s-%s Start:%s Consumed: %s [Total:%d Waiting:%d Running:%d Success:%d Fail:%d]"
    start = self.ist_start_time.strftime("%H:%M")
    consumed = (self.time_consumed or str(
        DatetimeUtils.time_diff_in_minutes(self.ist_start_time, DatetimeUtils.cur_ist_time()))) + "M"
    total = len(self.table_handlers)
    fail = len(self.fail_msgs)
    success = len(self.success_msgs)
    running = len(self.incomplete_msgs) - self.waiting_count

    title = (title_format % (
    self.tags, ENV_PREFIX, self.date_str, str(self.hour), start, consumed, total, self.waiting_count, running, success,
    fail))
    return title + " " + title_append


def _generate_body(content):
        body_prepend=""
        body_append=""
        body = "<html><head></head><body>" + _handle_new_line(str(body_prepend)) + "%s" + _handle_new_line(
            str(body_append)) + "</body></html>"
        body_success = "<br/><br/>\n<table class='success' style='border-collapse: collapse;background-color: rgba(0,255,0,0.1);border: 1px solid black;'>"
        body_success += _create_html_row(["S.No."],
                                              True) + "%s</table><br/>"
        body_success = (body_success % ''.join(map(str, content)))
        css = ""
        return (body % (body_success + css + body_append))


def _create_html_row(attributes, heading=False):
        row = ""
        col_format = "<td style='border: 1px solid black;'>%s</td>" if not heading else "<th style='border: 1px solid black;'>%s</th>"
        for attribute in attributes:
            row += (col_format % attribute)
        return "<tr style='border: 1px solid black;'>%s</tr>" % row

def send_if_required( to, title, body, title_append=""):
        body=_generate_body(body)
        print body
        # send mail only if there is a failure
        _send_mail(to, title, body)

def _handle_new_line( txt):
        return txt.replace("\n", "<br/>")


def _send_mail(to, title, desc, attach_filepaths=None):
        EmailHandler().send_email(to, title, desc)


