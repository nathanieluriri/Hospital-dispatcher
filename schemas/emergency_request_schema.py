from schemas.general_imports import *
from enum import Enum

class EmergencyPriority(str, Enum):
    critical = "critical"
    high = "high"
    moderate = "moderate"
    low = "low"

class EmergencySeverity(str, Enum):
    cardiac_arrest = "cardiac_arrest"
    minor_injury = "minor_injury"
    severe_trauma = "severe_trauma"
    respiratory_failure = "respiratory_failure"
    major_burn = "major_burn"
    stroke = "stroke"
    unconscious = "unconscious"
    allergic_reaction = "allergic_reaction"
    active_bleeding = "active_bleeding"
    fracture = "fracture"
    poisoning = "poisoning"
    seizure = "seizure"
    labor_and_delivery = "labor_and_delivery"
    chest_pain = "chest_pain"
    hypothermia = "hypothermia"
    heatstroke = "heatstroke"
    psychiatric_crisis = "psychiatric_crisis"
    drowning = "drowning"
    unknown = "unknown"
    
EMERGENCY_PRIORITY_MAP = {
    EmergencySeverity.cardiac_arrest: EmergencyPriority.critical,
    EmergencySeverity.respiratory_failure: EmergencyPriority.critical,
    EmergencySeverity.stroke: EmergencyPriority.critical,
    EmergencySeverity.unconscious: EmergencyPriority.critical,
    EmergencySeverity.drowning: EmergencyPriority.critical,
    EmergencySeverity.major_burn: EmergencyPriority.high,
    EmergencySeverity.severe_trauma: EmergencyPriority.high,
    EmergencySeverity.active_bleeding: EmergencyPriority.high,
    EmergencySeverity.allergic_reaction: EmergencyPriority.high,
    EmergencySeverity.poisoning: EmergencyPriority.high,
    EmergencySeverity.seizure: EmergencyPriority.high,
    EmergencySeverity.chest_pain: EmergencyPriority.high,
    EmergencySeverity.labor_and_delivery: EmergencyPriority.high,
    EmergencySeverity.fracture: EmergencyPriority.moderate,
    EmergencySeverity.heatstroke: EmergencyPriority.moderate,
    EmergencySeverity.hypothermia: EmergencyPriority.moderate,
    EmergencySeverity.psychiatric_crisis: EmergencyPriority.moderate,
    EmergencySeverity.minor_injury: EmergencyPriority.low,
    EmergencySeverity.unknown: EmergencyPriority.low,
}
 

    
class SubmitEmergencyRequestModelBase(BaseModel):
    severity:EmergencySeverity
    longitude:float
    latitude:float
class SubmitEmergencyRequestModel(SubmitEmergencyRequestModelBase):
    user_id:int
    request_time:int
class AssignedEmergencyRequestModel(SubmitEmergencyRequestModel):
    id:int
    assigned_ambulance_id:int
    dispatch_time:int
    dispatch_delay:int
    
class ResponedEmergencyRequestModel(AssignedEmergencyRequestModel):
    response_duration: int
    arrival_time: int
    
    
class EmergencyRequestOut(ResponedEmergencyRequestModel):
    id:int



class UnfinishedEmergencyRequestOut(BaseModel):
    id:int
    user_id:int
    severity:Optional[str]=None
    longitude:Optional[float]=None
    latitude:Optional[float]=None
    request_time:Optional[int]=None
    response_duration: Optional[int]=None
    travel_time: Optional[int]=None
    arrival_time: Optional[int]=None
    assigned_ambulance_id:Optional[int]=None
    dispatch_time:Optional[int]=None
    dispatch_delay:Optional[int]=None