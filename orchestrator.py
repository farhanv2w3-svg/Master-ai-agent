from gemini_client import GeminiClient
from registry import AgentRegistry
from models import AgentSpecification
from safety import secure_path
import json

class MasterOrchestrator:
    def __init__(self):
        self.ai = GeminiClient()
        self.registry = AgentRegistry()

    def process_instruction(self, instruction: str) -> dict:
        results = []
        try:
            # 1. UNDERSTAND & PLAN
            specs_data = self.ai.plan_agents(instruction)
            
            for spec_dict in specs_data:
                # 2. CREATE SPECIFICATION
                spec = AgentSpecification(**spec_dict)
                
                # 3. GENERATE AGENT ARCHITECTURE & CODE
                agent_code = self.ai.generate_agent_code(json.dumps(spec_dict))
                
                # 4. SECURE PATH & SAVE (Registering the project)
                project_dir = secure_path(spec.name)
                main_py_path = secure_path(spec.name, "main.py")
                spec_json_path = secure_path(spec.name, "spec.json")
                
                with open(main_py_path, "w", encoding="utf-8") as f:
                    f.write(agent_code)
                with open(spec_json_path, "w", encoding="utf-8") as f:
                    json.dump(spec_dict, f, indent=4)
                    
                # 5. REVIEW & VALIDATE (Simulated in MVP via schema validation and successful file write)
                
                # 6. REGISTER
                agent_id = self.registry.register_agent(spec, project_dir)
                
                results.append({
                    "name": spec.name,
                    "status": "READY",
                    "id": agent_id
                })
                
            return {"status": "success", "message": "Agents planned, generated, and registered successfully.", "agents": results}
        
        except Exception as e:
            return {"status": "error", "message": str(e)}