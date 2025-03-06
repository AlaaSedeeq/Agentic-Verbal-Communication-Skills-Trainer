def route_conflit_story_start(state):
    if not state["latest_module"].data.scenario:
        return "conflict_scenario_not_generated"
    return "user_input"

def route_conflict_validation(state):
    if state["latest_module"].data.user_transcript_validation.is_valid:
        return "valid_response"
    return "invalid_response"
