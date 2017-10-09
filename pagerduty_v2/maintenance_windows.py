import requests
import arrow
import json


def start_maintenance_window(api_key,
                             service_id,
                             email,
                             **kwargs):
    """
    Starts maintenance windows in your local timezone

    positional:
    :param api_key: PagerDuty API v2 key
    :type  api_key: str
    :param service_id: on the Services page, in the URL, the last set of characters after the / is the service ID
    :type  service_id: str
    :param email: valid email address associated with PagerDuty account
    :type  email: str

    **kwargs:
    :param description: description of maintenance
    :type  description: str
    :param start_time: timestamp for start of maintenance window (eg. 2017-10-15T14:33:32-05:00). Defaults to 'now'.
    :type  start_time: str
    :param duration: number of hours the maintenance window will remain open unless manually closed
    :type  duration: str or int
    :param timezone: eg. US/Central
    :type  timezone: str

    :return: JSON output from POST
    :rtype:  json
    """

    description = kwargs.get('description', None)
    start_time = kwargs.get('start_time', 'now')
    duration = kwargs.get('duration', 1)
    timezone = kwargs.get('timezone', 'US/Central')

    if 'now' in start_time:
        start_time = arrow.now(timezone)
    else:
        get_time = arrow.get(start_time)
        start_time = get_time.to(timezone)

    end_time = start_time.shift(hours=+int(duration))

    url = "https://api.pagerduty.com/maintenance_windows"
    headers = {
        "Content-type": "application/json",
        "Accept": "application/vnd.pagerduty+json;version=2",
        "From": email,
        "Authorization": "Token token={0}".format(api_key)
    }

    data = {
        "maintenance_window": {
            "type": "maintenance_window",
            "start_time": "{0}".format(start_time),
            "end_time": "{0}".format(end_time),
            "description": "{0}".format(description),
            "services": [
                {
                    "id": "{0}".format(service_id),
                    "type": "service_reference"
                }
            ]
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if not response.ok:
        response_json = None
        try:
            response_json = response.json()
        except Exception as e:
            exception = str(e)
        finally:
            msg = {
                "message": "failed to start maintenance window.",
                "status_code": response.status_code,
                "api_response": {
                    "json": response_json
                } if response_json else { "exception": exception }
            }
            return msg
    json_out = response.json()

    return json_out


def stop_maintenance_window(api_key,
                            service_id,
                            id):
    """
    Stops maintenance windows

    positional:
    :param api_key: PagerDuty API v2 key
    :type  api_key: str
    :param service_id: on the Services page, in the URL, the last set of characters after the / is the service ID
    :type  service_id: str
    :param id: maintenance window id to stop
    :type  id: str

    :return: Success/Failure
    :rtype:  json
    """

    url = "https://api.pagerduty.com/maintenance_windows/{0}".format(id)
    headers = {
        "Accept": "application/vnd.pagerduty+json;version=2",
        "Authorization": "Token token={0}".format(api_key)
    }

    response = requests.delete(url, headers=headers)

    if not response.ok:
        response_json = None
        try:
            response_json = response.json()
        except Exception as e:
            exception = str(e)
        finally:
            msg = {
                "message": "failed to stop maintenance window.",
                "status_code": response.status_code,
                "api_response": {
                    "json": response_json
                } if response_json else { "exception": exception }
            }
            return msg

    return { "maintenance_window": "{0} stopped successfully".format(id) }
