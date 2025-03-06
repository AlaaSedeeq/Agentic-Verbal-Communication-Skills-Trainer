import json
from pathlib import Path
from datetime import datetime
from typing import Union

from src.graph.state import TrainingModuleState, AssessmentModuleState

class SessionTracker:
    def __init__(self, base_dir: str = ""):
        self.base_dir = Path(base_dir) if base_dir else Path("data").joinpath("user_sessions")
        self.base_dir.mkdir(exist_ok=True)

    def _get_user_dir(self, user_id: str) -> Path:
        user_dir = self.base_dir / user_id
        user_dir.mkdir(exist_ok=True)
        return user_dir

    def _generate_session_filename(self) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"session_{timestamp}.json"

    def save_session(
        self,
        user_id: str,
        module_state: Union[TrainingModuleState, AssessmentModuleState],
        session_metadata: dict = None
    ) -> Path:
        user_dir = self._get_user_dir(user_id)
        session_file = user_dir / self._generate_session_filename()

        session_data = {
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
            "module_state": module_state.model_dump(),
            "metadata": session_metadata or {}
        }

        # Convert all datetime objects in session_metadata
        if session_metadata:
            session_data["metadata"] = {
                key: (value.isoformat() if isinstance(value, datetime) else value)
                for key, value in session_metadata.items()
            }

        with open(session_file, "w") as f:
            json.dump(session_data, f, indent=2)

        return session_file


    @classmethod
    def load_session(cls, user_id: str, session_file: str) -> dict:
        session_path = cls.base_dir / user_id / session_file
        with open(session_path) as f:
            return json.load(f)
