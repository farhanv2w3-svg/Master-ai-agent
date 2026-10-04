import os
from config import Config

def secure_path(agent_name: str, filename: str = "") -> str:
    """
    Prevents path traversal attacks (e.g., ../../etc/passwd).
    Ensures all generated files stay strictly inside their designated agent folder.
    """
    safe_agent_name = "".join(c for c in agent_name if c.isalnum() or c in ("_", "-")).strip()
    agent_dir = os.path.abspath(os.path.join(Config.AGENTS_DIR, safe_agent_name))
    
    if not agent_dir.startswith(os.path.abspath(Config.AGENTS_DIR)):
        raise PermissionError("Path traversal blocked at directory level.")
        
    if not os.path.exists(agent_dir):
        os.makedirs(agent_dir)
        
    if filename:
        safe_filename = os.path.basename(filename) # Strip any directory paths from the filename
        full_path = os.path.abspath(os.path.join(agent_dir, safe_filename))
        if not full_path.startswith(agent_dir):
            raise PermissionError("Path traversal blocked at file level.")
        return full_path
        
    return agent_dir