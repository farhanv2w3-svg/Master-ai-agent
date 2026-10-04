from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

class AgentSpecification(BaseModel):
    name: str
    domain: str
    purpose: str
    capabilities: List[str]
    inputs: List[str]
    outputs: List[str]
    tools: List[str]

class AgentRecord(BaseModel):
    id: str
    name: str
    description: str
    domain: str
    capabilities: str  # Stored as comma-separated string
    version: str
    status: str
    project_path: str
    creation_time: str

class UserRequest(BaseModel):
    instruction: str