import requests
import json


def get_incident(api_key, **kwargs):
    """
    get incident details.

    positional:
    :param api_key: PagerDuty API v2 key
    :type  api_key: str

    **kwargs:
    :param id: unique incident id or incident number
    :type  id: str

    :return: JSON output from GET
    :rtype:  json
    """

    id = kwargs.get('id', None)

    url = "https://api.pagerduty.com/incidents/{0}".format(id)
    headers = {
        "Content-type": "application/json",
        "Accept": "application/vnd.pagerduty+json;version=2",
        "Authorization": "Token token={0}".format(api_key)
    }

    if id:
        response = requests.get(url, headers=headers)

        if not response.ok:
            response_json = None
            try:
                response_json = response.json()
            except Exception as e:
                exception = str(e)
            finally:
                msg = {
                    "message": "failed to check current incident status.",
                    "status_code": response.status_code,
                    "api_response": {
                        "json": response_json
                    } if response_json else { "exception": exception }
                }
                return msg
        json_out = response.json()
        return json_out
    else:
        return { "incident": "incident id was not specified so nothing to check!" }


def create_incident(api_key,
                    service_id,
                    email,
                    escalation_policy_id=None,
                    **kwargs):
    """
    Creates incidents with status 'triggered'

    positional:
    :param api_key: PagerDuty API v2 key
    :type  api_key: str
    :param service_id: on the Services page, in the URL, the last set of characters after the / is the service ID
    :type  service_id: str
    :param email: valid email address associated with PagerDuty account
    :type  email: str
    :param escalation_policy_id: escalation policy id to associate with the incident (optional)
    :type  escalation_policy_id: str

    **kwargs:
    :param title: title or name of the incident to create
    :type  title: str
    :param details: body of the incident message
    :type  details: str
    :param priority_id: priority of this incident (optional)
    :type  priority_id: str

    :return: JSON output from POST
    :rtype:  json
    """

    title = kwargs.get('title')
    details = kwargs.get('details')
    priority_id = kwargs.get('priority_id', None)

    url = "https://api.pagerduty.com/incidents"
    headers = {
        "Content-type": "application/json",
        "Accept": "application/vnd.pagerduty+json;version=2",
        "From": email,
        "Authorization": "Token token={0}".format(api_key)
    }

    data = {
        "incident": {
            "type": "incident",
            "title": title,
            "service": {
                "id": service_id,
                "type": "service_reference"
            },
            "priority": {
                "id": priority_id,
                "type": "priority_reference"
            } if priority_id else {},
            "body": {
                "type": "incident_body",
                "details": details
            },
            "escalation_policy": {
                "id": escalation_policy_id,
                "type": "escalation_policy_reference"
            } if escalation_policy_id else {}
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
                "message": "failed to create incident.",
                "status_code": response.status_code,
                "api_response": {
                    "json": response_json
                } if response_json else { "exception": exception }
            }
            return msg
    json_out = response.json()
    return json_out


def update_incident(api_key,
                    email,
                    **kwargs):
    """
    Updates incident status

    positional:
    :param api_key: PagerDuty API v2 key
    :type  api_key: str
    :param email: valid email address associated with PagerDuty account
    :type  email: str

    **kwargs:
    :param id: incident id to update
    :type  id: str
    :param status: status to assign to incident, either 'acknowledged' or 'resolved'
    :type  status: str

    :return: JSON output from PUT
    :rtype:  json
    """

    id = kwargs.get('id', None)
    status = kwargs.get('status')

    url = "https://api.pagerduty.com/incidents/{0}".format(id)
    headers = {
        "Content-type": "application/json",
        "Accept": "application/vnd.pagerduty+json;version=2",
        "From": email,
        "Authorization": "Token token={0}".format(api_key)
    }

    data = {
        "incident": {
            "type": "incident_reference",
            "status": status
        }
    }

    response = requests.put(url, headers=headers, data=json.dumps(data))

    if not response.ok:
        response_json = None
        try:
            response_json = response.json()
        except Exception as e:
            exception = str(e)
        finally:
            msg = {
                "message": "failed to update incident {0}.".format(id),
                "status_code": response.status_code,
                "api_response": {
                    "json": response_json
                } if response_json else { "exception": exception }
            }
            return msg
    json_out = response.json()
    return json_out
