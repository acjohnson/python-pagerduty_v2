from pagerduty_v2.incidents import *
from pagerduty_v2.maintenance_windows import *


def v2(**kwargs):
    """
    Example **kwargs structure:

        {
            "api_key": "str",
            "service_id": "str",
            "email": "str",
            "escalation_policy_id": "str",
            "incidents": {
                "id": "str",
                "title": "str",
                "status": "str",
                "details": "str",
                "priority_id": "str"
            },
            "maintenance_windows": {
                "id": "str",
                "start_time": "str",
                "duration": "str",
                "description": "str",
                "timezone": "str",
                "action": "str"
            }
        }
    """

    api_key = kwargs.get('api_key')
    service_id = kwargs.get('service_id')
    email = kwargs.get('email')
    escalation_policy_id = kwargs.get('escalation_policy_id', None)

    for request_type, args in kwargs.items():
        if 'incidents' in request_type:
            if args.get('id') and args.get('status') is None:
                result = get_incident(api_key,
                                      **args)
                return result
            elif args.get('id') and args.get('status'):
                result = update_incident(api_key,
                                         email,
                                         **args)
                return result
            if 'triggered' in args.get('status'):
                result = create_incident(api_key,
                                         service_id,
                                         email,
                                         escalation_policy_id,
                                         **args)
                return result

        if 'maintenance_windows' in request_type:
            if 'start' in args.get('action'):
                result = start_maintenance_window(api_key,
                                                  service_id,
                                                  email,
                                                  **args)
                return result

            if 'stop' in args.get('action'):
                result = stop_maintenance_window(api_key,
                                                 service_id,
                                                 id=args.get('id'))
                return result


if __name__ == '__main__':
    v2(**kwargs)
