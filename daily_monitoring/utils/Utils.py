import logging
from daily_monitoring.settings import *
import yaml
import requests



class Utils:
    logger = logging.getLogger(__name__)

    def _json_response_handler(response):
        response.raise_for_status()
        # because json loads strings in unicode format whereas yaml safe_load in ASCII
        return yaml.safe_load(response.content)

    def job_completed_search(starts_with):
        response = requests.get(HIVE_TO_REDSHIFT_JOB_COMPLETED_SEARCH_API_URL, params={'starts_with': starts_with})
        return _json_response_handler(response)


