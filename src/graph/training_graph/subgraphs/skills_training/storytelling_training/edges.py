def route_story_start(state):
    #vaidate UI got the topic from user first
    if not state.get("latest_module").data.story_prompt:
        return "story_prompt_not_generated"
    return "user_input"

def route_story_validation(state):
    if state["latest_module"].data.user_transcript_validation.is_valid:
        return "valid_story"
    return "invalid_story"
