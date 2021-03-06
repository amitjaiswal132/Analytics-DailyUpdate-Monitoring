import sys
from array import array
from optparse import OptionParser
import logging.config
import signal
from datetime import timedelta, datetime
from analytics_common.utils.io_utils import IOUtils
from analytics_common.utils.datetime_utils import DatetimeUtils
from daily_monitoring.settings import *
from daily_monitoring.handlers import ReportHandler
from daily_monitoring.utils import Utils
import yaml
import requests


def parse_arguments():
    parser = OptionParser()
    parser.add_option("-d", "--day",
                      dest="day", default=None,
                      help="yyyy-mm-dd day you want to import [default: %default yesterday]")
    parser.add_option("--hour",
                      dest="hour", default=None, type="int",
                      help="utc hour for which the updates should happen [default: %default current hour]")
    parser.add_option("--redshift_table",
                      dest="redshift_table", default=None,
                      help="Pass the table name to check [default: %default]")
    parser.add_option("--email",
                      dest="email", default=False, action="store_true",
                      help="if set then will send emails else not  [default: %default]")
    parser.add_option("-n", "--nagios-hour-threshold",
                      dest="nagios_hour_threshold", default=12, type="int",
                      help="queries scheduled after this hour (ist) will not trigger nagios [default: %default]")
    (options,args) = parser.parse_args()

    return parser, options


def main():
    #logger.debug("sys.argv: %s", sys.argv)
    parser, options = parse_arguments()
    additional_msg = "Executing hourly run status check"
    content = []
    title = ""
    dt_str = DatetimeUtils.cur_utc_time()

    # it should be called in finally block
    def _finally_handler(title, content):
        ReportHandler.send_if_required(EMAIL_TO, title, content)


    def signal_term_handler(signal, frame):
        msg = "got SIGTERM, signal: %s" %(signal)
        #logger.error(msg)
        mail_additional_msg = additional_msg + "\n" + msg

    def _json_response_handler(response):
        response.raise_for_status()
        # because json loads strings in unicode format whereas yaml safe_load in ASCII
        return yaml.safe_load(response.content)

    def job_completed_search(starts_with):
        response = requests.get(HIVE_TO_REDSHIFT_JOB_COMPLETED_SEARCH_API_URL, params={'starts_with': starts_with})
        return _json_response_handler(response)

    # set SIGTERM (on kill) signal handler
    # just to make sure in case of kill also table_handlers are terminated properly and failure mail sent
    signal.signal(signal.SIGTERM, signal_term_handler)
    try:
        redshift_table = options.redshift_table if options.redshift_table is not None else "hourly_complete_status"
        logger.info( redshift_table)
        dt_str=DatetimeUtils.cur_utc_time()

        title = "v2:Redshift Upload hourly Status : %s day : %s " % (dt_str.strftime("%Y-%m-%d"), str(dt_str.hour))
        if options.day is not None and options.hour is not None:
            date_str = options.day if options.day is not None else str(DatetimeUtils.cur_utc_time().date())
            hour = options.hour if options.hour is not None else str(DatetimeUtils.cur_utc_time().hour)
            dt_str = date_str.replace(hour=hour)
        for delta in range(SLA_HOURLY_JOB_STATUS,24+SLA_HOURLY_JOB_STATUS):
            date_str = dt_str - timedelta(hours=delta)
            check_dt_str = "%s" %(date_str.strftime("%Y-%m-%d-%H"))
            search_name = HIVE_TO_REDSHIFT_JOB_COMPLETED_NAME_FORMAT % (HIVE_TO_REDSHIFT_HOURLY_JOB_STATUS, check_dt_str)
            logger.info( len(job_completed_search(search_name)))
            if len(job_completed_search(search_name)) == 0:
                content.append( "\n Hourly status check failed for date: %s hour: %s" % (date_str.strftime("%Y-%m-%d"), str(date_str.hour)))

        if len(content):
           message = "Hourly status check failed date: %s hour: %s" % (date_str.strftime("%Y-%m-%d"), str(date_str.hour))
           day_str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
           file_path = NAGIOS_FILE_FORMAT % (day_str)
           IOUtils.write(file_path, message)

    except BaseException as e:
        message = "Hourly status check failed date: %s hour: %s" % (date_str.strftime("%Y-%m-%d"), str(date_str.hour))
        logger.info( "Message %s ", str(message))
        logger.error("Exception %s " , str(e))
        day_str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        file_path = NAGIOS_FILE_FORMAT % (day_str)
        IOUtils.write(file_path, message)
    finally:
       _finally_handler(title, content)

if __name__ == "__main__":
    IOUtils.create_file(LOG_FILEPATH)
    logging.config.fileConfig(LOG_CONFIG, disable_existing_loggers=False)
    logger = logging.getLogger(__name__)
    logger.info("LOG_FILEPATH: %s", LOG_FILEPATH)
    logger.info("LOG_FILEPATH : %s", LOG_FILEPATH)
    logger.info("LOG_CONFIG : %s", LOG_CONFIG)
    main()
