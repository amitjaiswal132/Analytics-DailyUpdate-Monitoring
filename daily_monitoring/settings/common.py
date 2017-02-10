import pkg_resources
import os
from datetime import datetime

BASE_DIR = os.path.join(pkg_resources.resource_filename(__name__, ""), "../..")
LOG_CONFIG = os.path.join(BASE_DIR, "logging.ini")

WRITE_DIR = "/tmp/AnalyticsDailyUpdate/"
LOG_FILEPATH = os.path.join(WRITE_DIR, "logs", datetime.now().strftime("%Y-%M-%H-%M-%S.log"))

HIVE_TO_REDSHIFTS_API_HOST = "http://analytics-staging.hike.in"
HIVE_TO_REDSHIFT_JOB_COMPLETED_SEARCH_API_URL = HIVE_TO_REDSHIFTS_API_HOST + "/job_completed/search"
HIVE_TO_REDSHIFT_JOB_COMPLETED_NAME_FORMAT = "hive_to_redshift_%s-%s"
HIVE_TO_REDSHIFT_HOURLY_JOB_STATUS = "user_sticker_activity"
SLA_HOURLY_JOB_STATUS = 4
EMAIL_TO = "amitj@hike.in"
ENV_PREFIX = "Staging"

NAGIOS_FILE_FORMAT = "/tmp/nagios_check_files/daily_update_failed-%s"

