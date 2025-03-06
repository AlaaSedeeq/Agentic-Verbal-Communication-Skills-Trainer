from langchain_core.messages import AIMessage, HumanMessage
from src.session.session_tracker import SessionTracker
from .chains import (
    conflict_scenario_chain,
    conflict_diplomacy_evaluator,
    conflict_validation_chain,
    conflict_feedback_chain
)

def conflict_generate_scenario(state):
    category = state["latest_module"].data.category
    scenario = conflict_scenario_chain.invoke({
        "category": category
    })

    state["latest_module"].data.scenario = scenario.content
    state["messages"].append(HumanMessage(content="Category: " + category))
    state["messages"].append(scenario)

    return state

def conflict_validate_response(state):
    script = next(msg.content for msg in state["messages"] if isinstance(msg, HumanMessage))
    category = state["latest_module"].data.category
    validation = conflict_validation_chain.invoke({
        "category": category,
        "scenario": state["latest_module"].data.scenario,
        "response": script
    })

    if validation.is_valid:
        state["latest_module"].data.user_transcript_validation = validation
        state["latest_module"].data.user_input = script

    return state

def conflict_evaluate_diplomacy(state):
    script = next(msg.content for msg in state["messages"] if isinstance(msg, HumanMessage))
    evaluation = conflict_diplomacy_evaluator.invoke({
        "scenario": state["latest_module"].data.scenario,
        "response": script
    })
    state["latest_module"].data.user_transcript_evaluation.diplomacy = evaluation
    return state

def conflict_generate_feedback(state):
    feedback = conflict_feedback_chain.invoke({
        "diplomacy": state["latest_module"].data.user_transcript_evaluation.diplomacy
    })
    state["messages"].append(feedback)
    state["latest_module"].data.user_transcript_evaluation.feedback = feedback.content
    return state

def conflict_followup(state):
    guidance = state["latest_module"].data.user_transcript_validation.followup_message
    state["messages"].append(AIMessage(
        content=guidance,
        additional_kwargs={
            "retry_instructions": "Revise your response focusing on: " +
            ", ".join(state["latest_module"].data.user_transcript_validation.invalid_reasons)
        }
    ))
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
