from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.messages.tool import ToolCall

from src.session import SessionTracker
from .chains import (
    impromptu_topic_chain,
    impromptu_validation_chain,
    impromptu_structure_analyzer,
    impromptu_fluency_evaluator,
    impromptu_feedback_chain,
    impromptu_followup_chain
    )

def impromptu_generate_topic(state):

    topic_name = state["latest_module"].data.topic

    impromptu_topic = impromptu_topic_chain.invoke({"category": topic_name})

    state["latest_module"].data.topic_title = impromptu_topic.content

    state["messages"].append(HumanMessage(content="Topic type: " + topic_name))
    state["messages"].append(impromptu_topic)

    return state


def impromptu_validation(state):
    # print("User: ", state["messages"][-1].content)
    script = next(msg.content for msg in state["messages"] if isinstance(msg, HumanMessage))
    validation = impromptu_validation_chain.invoke({
            "topic": state["latest_module"].data.topic_title,
            "transcript": script
        })

    if validation.is_valid:
        state["latest_module"].data.user_transcript_validation = validation
        state["latest_module"].data.user_input = script

    return state

def impromptu_followup(state):
    script = next(msg.content for msg in state["messages"] if isinstance(msg, HumanMessage))

    response = impromptu_followup_chain.invoke({
            "invalid_reasons": str(state['latest_module'].data.user_transcript_validation),
            "topic": state['latest_module'].data.topic,
            "transcript": script
        })

    state["messages"].append(response)

    return state

def impromptu_analyze_structure(state):
    script = next(msg.content for msg in state["messages"] if isinstance(msg, HumanMessage))

    analysis = impromptu_structure_analyzer.invoke({"transcript": script})

    # json_response, json_valid = validate_response(analysis.content, ImpromptuStructureEvaluationResponse, 5)

    state["latest_module"].data.user_transcript_evaluation.structure = analysis

    return state

def impromptu_evaluate_fluency(state):
    script = next(msg.content for msg in state["messages"] if isinstance(msg, HumanMessage))

    fluency = impromptu_fluency_evaluator.invoke({"transcript": script})

    # json_response, json_valid = validate_response(fluency.content, ImpromptuFluencyEvaluationResponse, 5)

    state["latest_module"].data.user_transcript_evaluation.fluency = fluency

    return state

def impromptu_feedback(state):
    feedback = impromptu_feedback_chain.invoke({
        "structure": state["latest_module"].data.user_transcript_evaluation.structure,
        "fluency": state["latest_module"].data.user_transcript_evaluation.fluency,
        "feedback": state["latest_module"].data.user_transcript_evaluation.feedback
    })

    state["messages"].append(feedback)
    state["latest_module"].data.user_transcript_evaluation.feedback = feedback.content

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
