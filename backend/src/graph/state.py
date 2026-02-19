import operator
from typing import Annotated, List, Dict, Optional, Any, TypedDict

# Defin the schema for a single  compliance result

class ComplianceIssue(TypedDict):
    category: str   
    description: str    # Specific detail of violation
    severity: str   # Critical | Warning
    timestamp: Optional[str]

# define the global graph state
class VideoAudioState(TypedDict):
    '''
    Defines the data schema for langgraph execution content
    '''

    # Input parameters
    video_url: str
    video_id: str

    # Ingestion and extraction data
    local_file_path: Optional[str]
    video_metadata: Dict[str,Any] # {"duration": 120, "resolution": "1920x1080", "format": "mp4"}