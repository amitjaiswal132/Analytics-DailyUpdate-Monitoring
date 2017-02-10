
from daily_monitoring.settings.common import *

WRITE_DIR = "/mnt2/AnalyticsDailyUpdate/"
LOG_FILEPATH = os.path.join(WRITE_DIR, "logs", datetime.now().strftime("%Y-%M-%H-%M-%S.log"))
HIVE_TO_REDSHIFTS_API_HOST = "http://analytics.hike.in"
EMAIL_TO = "amitj@hike.in"
ENV_PREFIX = "prod"

NAGIOS_FILE_FORMAT = "/var/log/nagios_check_files/daily_update_failed-%s"
