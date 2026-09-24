from typing import Tuple, Optional
from backend.models import ComplianceStatus

class RuleEngine:
    @staticmethod
    def normalize_unit(value: float, unit: Optional[str]) -> Tuple[float, str]:
        if not unit:
            return value, ""
        
        u = unit.strip().lower()
        if u in ["tb", "terabyte"]:
            return value * 1024.0, "gb"
        elif u in ["gb", "gigabyte"]:
            return value, "gb"
        elif u in ["mb", "megabyte"]:
            return value / 1024.0, "gb"
            
        if u in ["cm"]:
            return value / 2.54, "inch"
        if u in ['"', "inch", "inç"]:
            return value, "inch"

        return value, u

    @classmethod
    def evaluate_numeric(
        cls, 
        required_val: float, 
        req_unit: Optional[str], 
        actual_val: Optional[float], 
        act_unit: Optional[str], 
        operator: str
    ) -> ComplianceStatus:
        if actual_val is None:
            return ComplianceStatus.UNKNOWN

        norm_req, u_req = cls.normalize_unit(required_val, req_unit)
        norm_act, u_act = cls.normalize_unit(actual_val, act_unit)

        if u_req != u_act and u_req != "" and u_act != "":
            return ComplianceStatus.UNKNOWN

        if operator in [">=", "min", "asgari", "en az"]:
            return ComplianceStatus.PASS if norm_act >= norm_req else ComplianceStatus.FAIL
        elif operator in ["<=", "max", "azami", "en fazla"]:
            return ComplianceStatus.PASS if norm_act <= norm_req else ComplianceStatus.FAIL
        elif operator in ["==", "=", "equals"]:
            return ComplianceStatus.PASS if norm_act == norm_req else ComplianceStatus.FAIL

        return ComplianceStatus.UNKNOWN