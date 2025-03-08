from langchain_core.messages import AIMessage, HumanMessage

from src.graph.utils import get_llms
from src.session.session_tracker import SessionTracker
from src.graph.state import State
from .prompts import FEEDBACK_TEMPLATE
from .types import (
    PresentationAssessmentEvaluation,
    PresentationAssessmentData,
    InputValidation,
    ContentEvaluation,
    DeliveryEvaluation,
    StructureEvaluation
)
from .chains import (
    validation_chain,
    structure_analyzer,
    delivery_analyzer,
    content_analyzer
)

text_llm_1, _ = get_llms(temperature = 0.1)
text_llm_7, _ = get_llms(temperature = 0.7)

def validate_input(state: State) -> State:
    script = next(
        msg.content 
        for msg in reversed(state["messages"]) 
        if isinstance(msg, HumanMessage)
    )
    
    validation = validation_chain.invoke({"script": script})
    print(validation)
    
    if validation.is_valid:
        # Initialize proper assessment structure
        state["latest_module"].data.user_transcript_validation = validation
        state["latest_module"].data.user_input = script

    return state

def handle_invalid_input(state: State):
    validation = state["latest_module"].data.user_transcript_validation
    guidance = "\n".join([
        "Please refine your script:",
        *validation.issues,
        f"Guidance: {validation.correction_guidance}"
    ])
    
    state["messages"].append(AIMessage(
        content=guidance,
        metadata={"type": "input_correction"}
    ))
    return state

def initialize_assessment(state: State):
    script = next(msg.content for msg in state["messages"] if isinstance(msg, HumanMessage))
    
    # Initialize with proper nested structure
    state["latest_module"] = PresentationAssessmentData(
        script=script,
        data=PresentationAssessmentData(
            user_transcript_validation=InputValidation.example(),
            user_transcript_evaluation=PresentationAssessmentEvaluation(
                structure=StructureEvaluation.example(),
                delivery=DeliveryEvaluation.example(),
                content=ContentEvaluation.example(),
                feedback="Initial analysis in progress..."
            )
        )
    )
    return state


def analyze_structure(state: State):
    script = next(msg.content for msg in state["messages"] if isinstance(msg, HumanMessage))
    result = structure_analyzer.invoke({"script": script})
    state["latest_module"].data.user_transcript_evaluation.structure = result 
    return state

def analyze_delivery(state: State):
    script = next(msg.content for msg in state["messages"] if isinstance(msg, HumanMessage))
    result = delivery_analyzer.invoke({"script": script})
    state["latest_module"].data.user_transcript_evaluation.delivery = result
    return state

def analyze_content(state: State):
    script = next(msg.content for msg in state["messages"] if isinstance(msg, HumanMessage))
    result = content_analyzer.invoke({"script": script})
    state["latest_module"].data.user_transcript_evaluation.content = result
    return state

def generate_final_report(state: State):
    assessment = state["latest_module"].data
    scores = [
        assessment.user_transcript_evaluation.structure.intro_score,
        assessment.user_transcript_evaluation.structure.conclusion_score,
        assessment.user_transcript_evaluation.structure.transition_score,
        assessment.user_transcript_evaluation.delivery.pacing_score,
        assessment.user_transcript_evaluation.delivery.clarity_score,
        assessment.user_transcript_evaluation.content.relevance_score,
        assessment.user_transcript_evaluation.content.persuasiveness_score
    ]
    assessment.overall_score = round(sum(scores) / len(scores) * 2, 1)  # Scale to 10
    
    feedback = text_llm_7.invoke(
        FEEDBACK_TEMPLATE.format(
            intro=assessment.user_transcript_evaluation.structure.intro_score,
            conclusion=assessment.user_transcript_evaluation.structure.conclusion_score,
            transitions=assessment.user_transcript_evaluation.structure.transition_score,
            structure_comment=assessment.user_transcript_evaluation.structure.structure_comment,
            pacing=assessment.user_transcript_evaluation.delivery.pacing_score,
            clarity=assessment.user_transcript_evaluation.delivery.clarity_score,
            fillers=", ".join(assessment.user_transcript_evaluation.delivery.filler_words) or "None detected",
            relevance=assessment.user_transcript_evaluation.content.relevance_score,
            persuasion=assessment.user_transcript_evaluation.content.persuasiveness_score,
            vocab=assessment.user_transcript_evaluation.content.vocabulary_level,
            improvement1="Improve transitions between sections",
            improvement2="Reduce filler words",
            score=assessment.overall_score
        )
    )
    
    assessment.priority_improvements = [
        line.split(". ", 1)[1] for line in feedback.content.split("\n") 
        if line.startswith(("1.", "2."))
    ]
    
    state["messages"].append(AIMessage(
        content=feedback.content,
        metadata={"type": "assessment_report"}
    ))
    state["sessions"].append(state["latest_module"])
    return state

def session_update_tracker(state, config):

    import time
    from datetime import datetime

    tracker = SessionTracker()

    user_id = config["configurable"]["user_id"]
    thread_id = config["configurable"]["thread_id"]
    module = state["latest_module"]

    start_time = datetime.fromisoformat(module.start_time) if isinstance(module.start_time, str) else module.start_time
    module_time = (start_time - datetime.now()).total_seconds()
    module_time_formatted = str(time.strftime("%H%M%S", time.gmtime(module_time)))

    # Save session
    saved_path = tracker.save_session(
        user_id=user_id,
        module_state=module,
        session_metadata={
            "duration_seconds": module_time_formatted,
            "user_id": user_id,
            "thread_id": thread_id
        }
    )

    state["sessions"].append(state["latest_module"])

    return state
