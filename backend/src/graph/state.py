import operator
from typing import Annotated, List, Dict, Optional, Any, TypedDict

# Defin the schema for a single  compliance result
# Error Report
class ComplianceIssue(TypedDict):
    category: str   
    description: str    # Specific detail of violation
    severity: str   # Critical | Warning
    timestamp: Optional[str]

# define the global graph state
# This defines the state that gets passed aroind in the agentic workflow
class VideoAudioState(TypedDict):
    '''
    Defines the data schema for langgraph execution content
    Main container : holds all the information about the audit
    right from the initial URL to the final report
    '''

    # Input parameters
    video_url: str
    video_id: str

    # Ingestion and extraction data
    local_file_path: Optional[str]
    video_metadata: Dict[str,Any] # {"duration": 120, "resolution": "1920x1080", "format": "mp4"}
    transcript : Optional[str] # Fully extracted speech- to- text
    ocr_text : List[str]

    # analysis output
    # Stores the list of all the violations found by AI
    compliance_results : Annotated[List[ComplianceIssue], operator.add]

    # final deliverables
    final_status : str # PASS | FAIL
    final_report : str

    # system observability
    # errors : API timeouts, processing errors, etc.
    errors : Annotated[List[str], operator.add]