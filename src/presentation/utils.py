import json
import os
from datetime import datetime

from src.graph.state import State, AssessmentModuleState, TrainingModuleState 
from src.graph.graphs.presentation_assessment.types import (
    PresentationAssessmentData, ContentEvaluation, DeliveryEvaluation,
    InputValidation, PresentationAssessmentEvaluation, StructureEvaluation
    ) 
from src.graph.graphs.skills_training.imrpomptu_speaking.types import (
    ImpromptuData, ImpromptuEvaluation, ImpromptuFluencyEvaluationResponse, 
    ImpromptuStructureEvaluationResponse, ImpromptuValidationResponse
    )
from src.graph.graphs.skills_training.storytelling_training.types import (
    StoryData, StoryEngagementEvaluation, StoryEvaluation, 
    StoryNarrativeEvaluation, StoryValidationResponse)
from src.graph.graphs.skills_training.conflict_resolution.types import (
    ConflictDiplomacyEvaluation, ConflictEvaluation, ConflictResolutionData, 
    ConflictValidationResponse, ConflictDiplomacyEvaluation
    )

path = os.path.join("data", "users")
os.makedirs(path, exist_ok=True)
user_data_path = os.path.join(path, "users.json")

def inint_graph_state(session_state):
    if session_state.user_choices["module"] == "Presentation Assessment":
        state = State(
            messages=[],
            sessions=[],
            latest_module = AssessmentModuleState(
                name="Assessment",
                start_time=datetime.now().isoformat(),
                last_feedback=None,
                data=PresentationAssessmentData(
                    user_input="",
                    user_transcript_validation=InputValidation.example(),
                    user_transcript_evaluation=PresentationAssessmentEvaluation(
                        structure=StructureEvaluation.example(),
                        delivery=DeliveryEvaluation.example(),
                        content=ContentEvaluation.example(),
                        feedback=""
                    ),
                    overall_score=0.0,
                    priority_improvements=[]
                )
            )
        )

    else:
        if session_state.user_choices["skill"] == "Impromptu Speaking":
            state = State(
                messages = [],
                sessions = [],
                latest_module = TrainingModuleState(
                    name="impromptu",
                    data=ImpromptuData(
                        topic=session_state.user_choices.get("category"),
                        topic_title="",
                        user_input="",  # Added missing field
                        user_transcript_validation=ImpromptuValidationResponse(
                            is_valid=False, invalid_reasons=[], followup_message=""
                        ),
                        user_transcript_evaluation=ImpromptuEvaluation(
                            structure=ImpromptuStructureEvaluationResponse(
                                score=1, 
                                has_intro=False,
                                has_conclusion=False,
                                organization="chaotic",
                                key_strength="",
                                to_improve=""
                            ),
                            fluency=ImpromptuFluencyEvaluationResponse(
                                filler_words=0,
                                clarity="mumbled",
                                fluency_score=1
                            ),
                            feedback=""
                        )
                    )
            )
            )

        if session_state.user_choices["skill"] == "Storytelling":
            state = State(
                messages = [],
                sessions = [],
                latest_module = TrainingModuleState(
                    name="storytelling",
                    data=StoryData(
                        genre=session_state.user_choices.get("category"),
                        story_prompt="",
                        user_transcript_validation=StoryValidationResponse( 
                            is_valid=False,
                            invalid_reasons=[],
                            followup_message=""
                        ),
                        user_transcript_evaluation=StoryEvaluation( 
                            narrative=StoryNarrativeEvaluation(
                                narrative_score=1,
                                character_development=1,
                                plot_complexity=1,
                                literary_devices=[],
                                key_strength="",
                                to_improve=""
                            ),
                            engagement=StoryEngagementEvaluation(
                                engagement_score=1,
                                hook_quality="weak",
                                pacing_analysis="uneven",
                                reader_interest="low",
                                satisfaction="unsatisfying"
                            ),
                            feedback=""
                        )
                    )
                )
            )

        if session_state.user_choices["skill"] == "Conflict Resolution":
            state = state = State(
                messages = [],
                training_sessions = [],
                latest_module = TrainingModuleState(
                    name="conflict_resolution",
                    data=ConflictResolutionData(
                        category=session_state.user_choices.get("category"), 
                        scenario="",
                        user_transcript_validation=ConflictValidationResponse(  
                            is_valid=False,
                            invalid_reasons=[],
                            followup_message=""
                        ),
                        user_transcript_evaluation=ConflictEvaluation(  
                            diplomacy=ConflictDiplomacyEvaluation(
                                empathy_score=1,
                                clarity_score=1,
                                solution_focus=1,
                                professionalism="poor",
                                negative_indicators=[]
                            ),
                            feedback=""
                        )
                    )
                )
            )

    return state

def get_graph(user_choices):
    if user_choices["module"] == "Presentation Assessment":
        from src.graph.graphs.presentation_assessment.builder import build_presentation_assessment_graph
        return build_presentation_assessment_graph()

    if user_choices["skill"] == "Impromptu Speaking":
        from src.graph.graphs.skills_training.imrpomptu_speaking.builder import build_impromptu_sgraph
        return build_impromptu_sgraph()

    if user_choices["skill"] == "Storytelling":
        from src.graph.graphs.skills_training.storytelling_training.builder import build_storytelling_graph
        return build_storytelling_graph()

    if user_choices["skill"] == "Conflict Resolution":
        from src.graph.graphs.skills_training.conflict_resolution.builder import build_conflict_resolution_graph
        return build_conflict_resolution_graph()
    

# User authentication functions
def save_user_data(username, password):
    users = {}
    if os.path.exists(user_data_path):
        with open(user_data_path, "r") as f:
            users = json.load(f)
    users[username] = password
    with open(user_data_path, "w") as f:
        json.dump(users, f)

def verify_user(username, password):
    if not os.path.exists(user_data_path):
        return False
    with open(user_data_path, "r") as f:
        users = json.load(f)
    return users.get(username) == password


def get_config(username):
    import uuid
    thread_id = username + str(uuid.uuid4())
    return {
        "configurable": {
            "thread_id": thread_id,
            "user_id": username
        }
    }
