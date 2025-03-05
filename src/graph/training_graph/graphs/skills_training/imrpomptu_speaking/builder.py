from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from src.graph.training_graph.state import State
from .edges import (
    route_impromptu_start,
    route_validation
)
from .nodes import (
    impromptu_analyze_structure,
    impromptu_evaluate_fluency,
    impromptu_feedback,
    impromptu_followup,
    impromptu_generate_topic,
    impromptu_validation,
    session_update_tracker
    )

def build_graph():
    builder = StateGraph(State)

    # Add nodes
    # builder.add_node("init_session_state", init_session_state)
    builder.add_node("generate_topic", impromptu_generate_topic)
    builder.add_node("validate_impromptu", impromptu_validation)
    builder.add_node("followup", impromptu_followup)
    builder.add_node("analyze_structure", impromptu_analyze_structure)
    builder.add_node("evaluate_fluency", impromptu_evaluate_fluency)
    builder.add_node("generate_feedback", impromptu_feedback)
    builder.add_node("session_tracker", session_update_tracker)

    # Build workflow
    builder.add_conditional_edges(
            START,
            route_impromptu_start,
            {
                "topic_not_generated": "generate_topic",
                "user_input": "validate_impromptu"
                }
        )
    # builder.add_edge("init_session_state", "generate_topic")
    builder.add_edge("generate_topic", END)
    builder.add_conditional_edges(
        "validate_impromptu",
        route_validation,
        {
            "valid": "analyze_structure",
            "invalid": "followup"
        }
    )
    builder.add_edge("analyze_structure", "evaluate_fluency")
    builder.add_edge("evaluate_fluency", "generate_feedback")
    builder.add_edge("generate_feedback", "session_tracker")
    builder.add_edge("session_tracker", END)
    builder.add_edge("followup", END)

    checkpointer = MemorySaver()
    impromptu_graph = builder.compile(checkpointer=checkpointer)

    return impromptu_graph
