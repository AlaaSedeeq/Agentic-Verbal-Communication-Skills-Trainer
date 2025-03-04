from langgraph.graph.message import AIMessage, HumanMessage, ToolMessage
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
    return state

def story_validate(state):
    user_messages = [m for m in state["messages"] if isinstance(m, HumanMessage)]

    validation = story_validation_chain.invoke({
        "story": user_messages[-1].content,
        "genre": state["latest_module"].data.genre
    })
    state["latest_module"].data.user_transcript_validation = validation
    return state

def story_followup(state):
    user_messages = [m for m in state["messages"] if isinstance(m, HumanMessage)]

    response = story_followup_chain.invoke({
            "invalid_reasons": str(state['latest_module'].data.user_transcript_validation),
            "genre": state['latest_module'].data.genre,
            "story": user_messages[-1].content
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
    state["latest_module"].data.user_transcript_evaluation.feedback = feedback.content
    return state

def session_update_tracker(state, config):

    import time
    from datetime import datetime

    tracker = SessionTracker()

    user_id = config["configurable"]["user_id"]
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
        }
    )

    state["training_sessions"].append(state["latest_module"])

    return state
    # print(f"Session saved to: {saved_path}")
