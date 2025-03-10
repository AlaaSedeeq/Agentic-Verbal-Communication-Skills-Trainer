# Conditional edge
def route_impromptu_start(state):
    #vaidate UI got the topic from user first
    if not state.get("latest_module").data.topic_title:
        # print("Topic Title: ", state.get("latest_module").data.topic_title)
        return "topic_not_generated"

    return "user_input"

def route_validation(state):
    if state["latest_module"].data.user_transcript_validation.is_valid:
        return "valid"
    return "invalid"
