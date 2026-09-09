import time
from typing import Dict, Optional, Any
from copy import deepcopy

# In-memory storage for reputation and IOC data
_reputation: Dict[str, dict] = {}
_ioc: Dict[str, dict] = {}

def _now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def _initialize_data():
    global _reputation, _ioc
    _reputation = {}
    _ioc = {}

    # Known deterministic TI data
    _reputation["185.220.101.5"] = {
        "indicator": "185.220.101.5",
        "reputation": "malicious",
        "confidence": 0.95,
        "observed_at": "2026-09-09T09:00:00Z"
    }
    _reputation["10.0.5.45"] = {
        "indicator": "10.0.5.45",
        "reputation": "unknown",
        "confidence": 0.50,
        "observed_at": "2026-09-09T09:00:00Z"
    }

    # IOC details (optional, for enrichment)
    _ioc["IOC-001"] = {
        "ioc_id": "IOC-001",
        "indicator": "185.220.101.5",
        "malware_family": "BruteBot",
        "ttp_tags": ["T1110", "T1078"],
        "observed_at": "2026-09-09T09:00:00Z"
    }
    _ioc["IOC-002"] = {
        "ioc_id": "IOC-002",
        "indicator": "10.0.5.45",
        "malware_family": "MalwareX",
        "ttp_tags": ["T1204", "T1059"],
        "observed_at": "2026-09-09T09:00:00Z"
    }

def reputation_lookup(indicator: str) -> Optional[dict]:
    """Return reputation for an indicator."""
    rep = _reputation.get(indicator)
    if rep is None:
        return None
    rep_copy = deepcopy(rep)
    rep_copy["metadata"] = {
        "source": "cyber-ti",
        "observed_at": rep_copy["observed_at"],
        "data_version": 1,  # static version
        "retrieved_at": _now_iso()
    }
    return rep_copy

def ioc_details(ioc_id: str) -> Optional[dict]:
    """Return details for an IOC."""
    ioc = _ioc.get(ioc_id)
    if ioc is None:
        return None
    ioc_copy = deepcopy(ioc)
    ioc_copy["metadata"] = {
        "source": "cyber-ti",
        "observed_at": ioc_copy["observed_at"],
        "data_version": 1,
        "retrieved_at": _now_iso()
    }
    return ioc_copy

def threat_feed_summary() -> dict:
    """Return a summary of the threat feed (not required for lab)."""
    return {
        "total_indicators": len(_reputation),
        "malicious_count": sum(1 for r in _reputation.values() if r["reputation"] == "malicious"),
        "suspicious_count": sum(1 for r in _reputation.values() if r["reputation"] == "suspicious"),
        "unknown_count": sum(1 for r in _reputation.values() if r["reputation"] == "unknown"),
        "metadata": {
            "source": "cyber-ti",
            "observed_at": _now_iso(),
            "data_version": 1,
            "retrieved_at": _now_iso()
        }
    }

# Initialize data on module load
_initialize_data()