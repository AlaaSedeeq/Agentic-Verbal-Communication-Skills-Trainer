from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from src.graph.training_graph.state import State
from .edges import (
    route_conflit_story_start,
    route_conflict_validation
)
from .nodes import (
    conflict_followup, 
    conflict_generate_scenario,
    conflict_generate_feedback,
    conflict_validate_response,
    conflict_evaluate_diplomacy,
    session_update_tracker
    )

def build_graph():

    builder = StateGraph(State)

    # Add Conflict Resolution Nodes
    builder.add_node("generate_conflict_scenario", conflict_generate_scenario)
    builder.add_node("validate_conflict_response", conflict_validate_response)
    builder.add_node("evaluate_diplomacy", conflict_evaluate_diplomacy)
    builder.add_node("generate_conflict_feedback", conflict_generate_feedback)
    builder.add_node("conflict_followup", conflict_followup)
    builder.add_node("session_tracker", session_update_tracker)

    builder.add_conditional_edges(
        "validate_conflict_response",
        route_conflict_validation,
        {
            "valid_response": "evaluate_diplomacy",
            "invalid_response": "conflict_followup"
        }
    )

    # Conflict Resolution Workflow
    # builder.add_edge("generate_conflict_scenario", "validate_conflict_response")
    builder.add_edge("evaluate_diplomacy", "generate_conflict_feedback")
    builder.add_edge("generate_conflict_feedback", "session_tracker")
    builder.add_edge("generate_conflict_scenario", END)
    builder.add_edge("conflict_followup", END)
    builder.add_edge("session_tracker", END)

    # Connect to Main Graph
    builder.add_conditional_edges(
        START,
        route_conflit_story_start,
        {
            "conflict_scenario_not_generated": "generate_conflict_scenario",
            "user_input": "validate_conflict_response"
        }
    )

    # Compile Graph
    checkpointer = MemorySaver()
    conflict_graph = builder.compile(checkpointer=checkpointer)

    return conflict_graph
