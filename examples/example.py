from pagerduty_v2 import api as pagerduty


# Note: be sure to use an email address associated with your pagerduty account.
defaults = {
    "api_key": "secret",
    "service_id": "PL7MVQH",
    "email": "email@example.com",
    "escalation_policy_id": None
}

get_incident = {
    "incidents": {
        "id": "26"
    }
}

create_incident = {
    "incidents": {
        "title": "computer is on fire",
        "status": "triggered",
        "details": "testing",
        "priority_id": "P72DUUN"
    }
}

update_incident = {
    "incidents": {
        "id": "P321K6M",
        "status": "resolved"
    }
}

start_maintenance_window = {
    "maintenance_windows": {
        "id": None,
        "start_time": "now",
        "duration": "1",
        "description": "reason for maintenance",
        "action": "start",
        "timezone": "US/Central"
    }
}

stop_maintenance_window = {
    "maintenance_windows": {
        "id": "PRJB9HI",
        "action": "stop",
    }
}

data = defaults.copy()
data.update(create_incident)
print(pagerduty.v2(**data))
