from langgraph.graph import StateGraph
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from src.graph.state import State
from src.graph.utils import get_llms
from .nodes import (
    validate_input,
    analyze_structure,
    analyze_delivery,
    analyze_content,
    generate_final_report,
    handle_invalid_input,
    session_update_tracker
)
from .edges import route_validation

text_llm_1, _ = get_llms(temperature = 0.1)
text_llm_7, _ = get_llms(temperature = 0.7)


def build_presentation_assessment_graph():
    # ======== GRAPH SETUP ========
    builder = StateGraph(State)

    builder.add_node("validate_input", validate_input)
    builder.add_node("analyze_structure", analyze_structure),
    builder.add_node("analyze_delivery", analyze_delivery),
    builder.add_node("analyze_content", analyze_content),
    builder.add_node("generate_report", generate_final_report)
    builder.add_node("handle_invalid", handle_invalid_input)
    builder.add_node("session_tracker", session_update_tracker)

    # Set entry point
    builder.set_entry_point("validate_input")

    # Add conditional routing
    builder.add_conditional_edges(
        "validate_input",
        route_validation,
        {
            "valid": "analyze_structure",
            "invalid": "handle_invalid"
        }
    )

    # Connect analysis flow
    builder.add_edge("analyze_structure", "analyze_delivery")
    builder.add_edge("analyze_delivery", "analyze_content")
    builder.add_edge("analyze_content", "generate_report")
    builder.add_edge("generate_report", "session_tracker")
    builder.add_edge("handle_invalid", END)
    builder.add_edge("session_tracker", END)

    # Compile Graph
    checkpointer = MemorySaver()
    assessment_graph = builder.compile(checkpointer=checkpointer)

    return assessment_graph
