from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from src.graph.training_graph.state import State
from .nodes import (
    story_analyze_narrative,
    story_evaluate_engagement,
    story_generate_feedback,
    story_followup,
    story_generate_prompt,
    story_validate,
    session_update_tracker
    )
from .edges import (
    route_story_start,
    route_story_validation
)

def build_graph():
    # ======== Storytelling Graph ========
    builder = StateGraph(State)

    # Storytelling Workflow

    builder.add_node("generate_story_prompt", story_generate_prompt)
    builder.add_node("validate_story", story_validate)
    builder.add_node("analyze_narrative", story_analyze_narrative)
    builder.add_node("evaluate_engagement", story_evaluate_engagement)
    builder.add_node("generate_story_feedback", story_generate_feedback)
    builder.add_node("story_followup", story_followup)
    builder.add_node("session_tracker", session_update_tracker)

    builder.add_edge("generate_story_prompt", END)
    builder.add_edge("analyze_narrative", "evaluate_engagement")
    builder.add_edge("evaluate_engagement", "generate_story_feedback")
    builder.add_edge("generate_story_feedback", "session_tracker")
    builder.add_edge("session_tracker", END)
    builder.add_edge("story_followup", END)

    # Connect to Main Graph
    builder.add_conditional_edges(
        START,
        route_story_start,
        {
            "story_prompt_not_generated": "generate_story_prompt",
            "user_input": "validate_story"
        }
    )
    builder.add_conditional_edges(
        "validate_story",
        route_story_validation,
        {
            "valid_story": "analyze_narrative",
            "invalid_story": "story_followup"
        }
    )
    # Compile Graph
    checkpointer = MemorySaver()
    story_graph = builder.compile(checkpointer=checkpointer)

    return story_graph
