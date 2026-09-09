import time
from typing import Dict, List, Optional, Any
from copy import deepcopy

# In-memory storage for alerts and events
_alerts: Dict[str, dict] = {}
_events: Dict[str, List[dict]] = {}

def _now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def _initialize_data():
    global _alerts, _events
    # Reset state for deterministic initialization
    _alerts = {}
    _events = {}

    # INC-001: brute_force
    alert_id_1 = "INC-001"
    _alerts[alert_id_1] = {
        "alert_id": alert_id_1,
        "type": "brute_force",
        "source_ip": "185.220.101.5",
        "target": "web-server-01",
        "severity": "high",
        "timestamp": "2026-09-09T10:00:00Z"
    }
    _events[alert_id_1] = [
        {
            "event_id": "EVT-001-1",
            "timestamp": "2026-09-09T10:00:00Z",
            "type": "failed_login",
            "source_ip": "185.220.101.5",
            "target": "web-server-01",
            "username": "admin"
        },
        {
            "event_id": "EVT-001-2",
            "timestamp": "2026-09-09T10:00:01Z",
            "type": "failed_login",
            "source_ip": "185.220.101.5",
            "target": "web-server-01",
            "username": "admin"
        }
    ]

    # INC-002: malware
    alert_id_2 = "INC-002"
    _alerts[alert_id_2] = {
        "alert_id": alert_id_2,
        "type": "malware",
        "source_ip": "10.0.5.45",
        "target": "workstation-01",
        "severity": "critical",
        "timestamp": "2026-09-09T10:05:00Z"
    }
    _events[alert_id_2] = [
        {
            "event_id": "EVT-002-1",
            "timestamp": "2026-09-09T10:05:00Z",
            "type": "file_write",
            "source_ip": "10.0.5.45",
            "target": "workstation-01",
            "file_path": "C:\\temp\\malware.exe",
            "hash": "a1b2c3d4e5f6"
        }
    ]

    # INC-003: suspicious_account
    alert_id_3 = "INC-003"
    _alerts[alert_id_3] = {
        "alert_id": alert_id_3,
        "type": "suspicious_account",
        "account": "jsmith",
        "severity": "high",
        "timestamp": "2026-09-09T10:10:00Z"
    }
    _events[alert_id_3] = [
        {
            "event_id": "EVT-003-1",
            "timestamp": "2026-09-09T10:10:00Z",
            "type": "privilege_escalation",
            "account": "jsmith",
            "source_ip": "10.0.5.45",
            "target": "workstation-01"
        }
    ]

def list_alerts(filter_dict: Optional[Dict[str, Any]] = None) -> List[dict]:
    """Return a list of alerts, optionally filtered."""
    if filter_dict is None:
        filter_dict = {}
    results = []
    for alert in _alerts.values():
        match = True
        for key, value in filter_dict.items():
            if alert.get(key) != value:
                match = False
                break
        if match:
            # Return a deep copy with metadata
            alert_copy = deepcopy(alert)
            alert_copy["metadata"] = {
                "source": "cyber-soc",
                "observed_at": alert_copy["timestamp"],
                "data_version": 1,  # static version for deterministic data
                "retrieved_at": _now_iso()
            }
            results.append(alert_copy)
    return results

def get_alert(alert_id: str) -> Optional[dict]:
    """Return a specific alert by ID."""
    alert = _alerts.get(alert_id)
    if alert is None:
        return None
    alert_copy = deepcopy(alert)
    alert_copy["metadata"] = {
        "source": "cyber-soc",
        "observed_at": alert_copy["timestamp"],
        "data_version": 1,
        "retrieved_at": _now_iso()
    }
    return alert_copy

def get_event_chain(alert_id: str) -> List[dict]:
    """Return the chain of events for an alert."""
    events = _events.get(alert_id, [])
    event_copies = []
    for ev in events:
        ev_copy = deepcopy(ev)
        ev_copy["metadata"] = {
            "source": "cyber-soc",
            "observed_at": ev_copy["timestamp"],
            "data_version": 1,
            "retrieved_at": _now_iso()
        }
        event_copies.append(ev_copy)
    return event_copies

def search_logs(query: str, time_range: Optional[Dict[str, str]] = None) -> List[dict]:
    """Not implemented for this lab."""
    # For simplicity, we return empty list.
    return []

# Initialize data on module load
_initialize_data()