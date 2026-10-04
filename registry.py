import sqlite3
import uuid
from datetime import datetime
from config import Config
from models import AgentSpecification, AgentRecord

class AgentRegistry:
    def __init__(self):
        self.db_path = Config.DB_PATH
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS agents (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    description TEXT,
                    domain TEXT,
                    capabilities TEXT,
                    version TEXT,
                    status TEXT,
                    project_path TEXT,
                    creation_time TEXT
                )
            ''')

    def register_agent(self, spec: AgentSpecification, project_path: str) -> str:
        agent_id = str(uuid.uuid4())
        creation_time = datetime.now().isoformat()
        capabilities_str = ", ".join(spec.capabilities)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO agents (id, name, description, domain, capabilities, version, status, project_path, creation_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (agent_id, spec.name, spec.purpose, spec.domain, capabilities_str, "1.0", "READY", project_path, creation_time))
        return agent_id

    def update_status(self, agent_id: str, status: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('UPDATE agents SET status = ? WHERE id = ?', (status, agent_id))

    def get_all_agents(self) -> list[AgentRecord]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('SELECT * FROM agents ORDER BY creation_time DESC')
            return [AgentRecord(**dict(row)) for row in cursor.fetchall()]