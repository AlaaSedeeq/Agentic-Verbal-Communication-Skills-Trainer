from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.messages.tool import ToolCall

from src.session import SessionTracker
from .chains import (
    story_prompt_chain,
    story_validation_chain,
    story_narrative_analyzer,
    story_engagement_analyzer,
    story_feedback_chain,
    story_followup_chain
    )

def story_generate_prompt(state):

    genre = state["latest_module"].data.genre

    story_prompt = story_prompt_chain.invoke({"genre": genre})

    state["latest_module"].data.story_prompt = story_prompt.content
    state["messages"].append(HumanMessage(content="Genre: " + genre))
    state["messages"].append(story_prompt)

    return state

def story_validate(state):
    script = next(msg.content for msg in state["messages"] if isinstance(msg, HumanMessage))

    validation = story_validation_chain.invoke({
        "story": script,
        "genre": state["latest_module"].data.genre
    })

    if validation.is_valid:
        state["latest_module"].data.user_transcript_validation = validation
        state["latest_module"].data.user_input = script

    return state

def story_followup(state):
    script = next(msg.content for msg in state["messages"] if isinstance(msg, HumanMessage))

    response = story_followup_chain.invoke({
            "invalid_reasons": str(state['latest_module'].data.user_transcript_validation),
            "genre": state['latest_module'].data.genre,
            "story": script
        })

    state["messages"].append(response)

    return state

def story_analyze_narrative(state):
    analysis = story_narrative_analyzer.invoke({
        "story": state["messages"][-1].content
    })
    state["latest_module"].data.user_transcript_evaluation.narrative = analysis
    return state

def story_evaluate_engagement(state):
    evaluation = story_engagement_analyzer.invoke({
        "story": state["messages"][-1].content
    })
    state["latest_module"].data.user_transcript_evaluation.engagement = evaluation
    return state

def story_generate_feedback(state):
    feedback = story_feedback_chain.invoke({
        "narrative": state["latest_module"].data.user_transcript_evaluation.narrative,
        "engagement": state["latest_module"].data.user_transcript_evaluation.engagement
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
