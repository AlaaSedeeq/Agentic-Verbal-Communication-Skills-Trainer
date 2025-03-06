# from datetime import datetime
from langchain_core.messages import AIMessage, HumanMessage

# from src.graph.graphs.presentation_assessment.builder import build_presentation_assessment_graph
from src.graph.graphs.skills_training.imrpomptu_speaking.builder import build_impromptu_sgraph
# from src.graph.graphs.skills_training.storytelling_training.builder import build_storytelling_graph
# from src.graph.graphs.skills_training.conflict_resolution.builder import build_conflict_resolution_graph
# from src.utils.graph import save_graph_image
from src.graph.graphs.presentation_assessment.types import PresentationAssessmentData, ContentEvaluation, DeliveryEvaluation, InputValidation, PresentationAssessmentEvaluation, StructureEvaluation 
from src.graph.graphs.skills_training.imrpomptu_speaking.types import ImpromptuData, ImpromptuEvaluation, ImpromptuFluencyEvaluationResponse, ImpromptuStructureEvaluationResponse, ImpromptuValidationResponse
from src.graph.graphs.skills_training.storytelling_training.types import StoryData, StoryEngagementEvaluation, StoryEvaluation, StoryNarrativeEvaluation, StoryValidationResponse
from src.graph.graphs.skills_training.conflict_resolution.types import ConflictDiplomacyEvaluation, ConflictEvaluation, ConflictResolutionData, ConflictValidationResponse, ConflictDiplomacyEvaluation
from src.graph.state import State, AssessmentModuleState, TrainingModuleState 

impromptu_graph = build_impromptu_sgraph()
# storytelling_graph = build_storytelling_graph()
# conflict_resolution_graph = build_conflict_resolution_graph()
# presentation_assessment_graph = build_presentation_assessment_graph()

config = {
    "configurable": {
        "thread_id": "ipromptu_00",
        "user_id": "test_user"}
}
print(impromptu_graph.invoke({'messages': [HumanMessage(content='"Artificially Intelligent Decision Making: Balancing Objectivity with Human Values"', additional_kwargs={}, response_metadata={'token_usage': {'completion_tokens': 17, 'prompt_tokens': 68, 'total_tokens': 85, 'completion_time': 0.011198755, 'prompt_time': 0.011909386, 'queue_time': 0.019825121, 'total_time': 0.023108141}, 'model_name': 'llama-3.2-3b-preview', 'system_fingerprint': 'fp_a926bfdce1', 'finish_reason': 'stop', 'logprobs': None}, id='run-ff017cf1-f6cc-4329-b328-8a39ddaf4195-0', usage_metadata={'input_tokens': 68, 'output_tokens': 17, 'total_tokens': 85})], 'sessions': [], 'latest_module': TrainingModuleState(name='impromptu', data=ImpromptuData(topic='Ethics and Philosophy', topic_title='"Artificially Intelligent Decision Making: Balancing Objectivity with Human Values"', user_input='', user_transcript_validation=ImpromptuValidationResponse(is_valid=False, invalid_reasons=[], followup_message=''), user_transcript_evaluation=ImpromptuEvaluation(structure=ImpromptuStructureEvaluationResponse(score=1, has_intro=False, has_conclusion=False, organization='chaotic', key_strength='', to_improve=''), fluency=ImpromptuFluencyEvaluationResponse(filler_words=0, clarity='mumbled', fluency_score=1), feedback='')), attempts=0, start_time='2025-03-06T18:27:25.799810', last_feedback=None)}, config))
######################
### Presentation test
######################
# test_config = {
#     "configurable": {
#         "thread_id": "pres_test_1",
#         "user_id": "test_user"
#     }
# }

# state = State(
#     messages=[],
#     sessions=[],
#     latest_module = AssessmentModuleState(
#         name="Assessment",
#         start_time=datetime.now().isoformat(),
#         last_feedback=None,
#         data=PresentationAssessmentData(
#             user_input="",
#             user_transcript_validation=InputValidation.example(),
#             user_transcript_evaluation=PresentationAssessmentEvaluation(
#                 structure=StructureEvaluation.example(),
#                 delivery=DeliveryEvaluation.example(),
#                 content=ContentEvaluation.example(),
#                 feedback="Initial analysis in progress..."
#             ),
#             overall_score=0.0,
#             priority_improvements=[]
#         )
#     )
# )

# poor_script = """Um, so today I'll talk about... uh, climate change? 
# It's like, really important because... you know, the ice is melting? 
# We should do something maybe. Anyway, that's all I guess."""

# state["messages"].append(HumanMessage(content=poor_script))

# state = presentation_assessment_graph.invoke(state, test_config)

# good_script = """Good afternoon. Today we'll explore three key strategies for combating climate change.
# First, transitioning to renewable energy sources. Solar and wind power adoption has increased 40% since 2015.
# Second, sustainable agriculture practices. Regenerative farming can sequester up to 10 tons of CO2 per acre annually.
# Finally, policy interventions. Carbon pricing mechanisms have proven effective in 23 countries.
# In conclusion, by combining technological innovation, agricultural reform, and legislative action, 
# we can create a sustainable future. The time to act is now."""
# state["messages"].append(HumanMessage(content=good_script))
# state = presentation_assessment_graph.invoke(state, test_config)

# print(state)

######################
### Conflict test
######################
# thread_id = "conflict_01"
# user_id = "test_user"
# config = {
#     "recursion_limit": 30,
#     "configurable": {
#         "thread_id": thread_id,
#         "user_id": user_id
#     }``
# }

# # ======== Test 1: Failed Validation (Aggressive Response) ========
# state = {
#     "messages": [],
#     "training_sessions": [],
#     "latest_module": TrainingModuleState(
#         name="conflict_resolution",
#         data=ConflictResolutionData(
#             category="Workplace/Professional", 
#             scenario="",
#             user_transcript_validation=ConflictValidationResponse(  
#                 is_valid=False,
#                 invalid_reasons=[],
#                 followup_message=""
#             ),
#             user_transcript_evaluation=ConflictEvaluation(  
#                 diplomacy=ConflictDiplomacyEvaluation(
#                     empathy_score=1,
#                     clarity_score=1,
#                     solution_focus=1,
#                     professionalism="poor",
#                     negative_indicators=[]
#                 ),
#                 feedback=""
#             )
#         )
#     )
# }

# state = conflict_resolution_graph.invoke(state, config)
# print(state)
# state["messages"].append(HumanMessage(content="START"))
# state = conflict_resolution_graph.invoke(state, config)

# # Submit invalid response
# test_response_1 = "This is all your fault! You never listen to anyone's ideas!"
# state["messages"].append(HumanMessage(content=test_response_1))
# state = conflict_resolution_graph.invoke(state, config)

# # Submit valid response
# test_response_2 = """I understand this situation is frustrating for both of us.
# Could we schedule a time to review what's causing the delays?
# Maybe we can find a solution that works for everyone."""
# state["messages"].append(HumanMessage(content=test_response_2))
# state = conflict_resolution_graph.invoke(state, config)

######################
### Storytellling test
######################
# thread_id = "story_0000"
# user_id = "test_user"
# config = {
#     "recursion_limit": 30,
#     "configurable": {
#         "thread_id": thread_id,
#         "user_id": user_id
#     }
# }

# state = {
#     "messages": [],
#     "sessions": [],
#     "latest_module": TrainingModuleState(
#         name="storytelling",
#         data=StoryData(
#             genre="Personal Growth",
#             story_prompt="",
#             user_transcript_validation=StoryValidationResponse( 
#                 is_valid=False,
#                 invalid_reasons=[],
#                 followup_message=""
#             ),
#             user_transcript_evaluation=StoryEvaluation( 
#                 narrative=StoryNarrativeEvaluation(
#                     narrative_score=1,
#                     character_development=1,
#                     plot_complexity=1,
#                     literary_devices=[],
#                     key_strength="",
#                     to_improve=""
#                 ),
#                 engagement=StoryEngagementEvaluation(
#                     engagement_score=1,
#                     hook_quality="weak",
#                     pacing_analysis="uneven",
#                     reader_interest="low",
#                     satisfaction="unsatisfying"
#                 ),
#                 feedback=""
#             )
#         )
#     )
# }

# state = storytelling_graph.invoke(state, config)
# # print(state)
# state["messages"].append(HumanMessage(content="START"))
# state = storytelling_graph.invoke(state, config)
# print("\nGenerated Story Prompt:", state["latest_module"].data.story_prompt)

# # Submit invalid story (too short)
# test_story_1 = """It was a rainy day. I forgot my umbrella.
# I ran to the bus stop. Got wet. The end."""
# state["messages"].append(HumanMessage(content=test_story_1))
# state = storytelling_graph.invoke(state, config)

# # ======== Test 2: Successful Story Submission ========
# # Submit valid story
# test_story_2 = """The hospital monitor beeped steadily as I clutched my father's hand.
# At 16, I never imagined I'd be making life-altering decisions. His cancer diagnosis
# came like a summer storm - sudden and drenching. Dr. Martinez explained the treatment
# options, her voice softening when mentioning the risks.

# I remember the smell of antiseptic mixing with mom's lavender perfume as we debated.
# Uncle Mark argued for aggressive treatment, while Aunt Lisa worried about quality of life.
# My childhood memories of dad coaching soccer games clashed with the frail figure in the bed.

# In the end, we chose palliative care. Watching his peaceful final weeks taught me more
# about love and loss than any teenage experience should. Now I volunteer at the hospice,
# sharing our story to help others navigate these impossible choices."""

# state["messages"].append(HumanMessage(content=test_story_2))
# state = storytelling_graph.invoke(state, config)
# print(state)

######################
### Impromptu test
######################
# thread_id = "ipromptu_00"
# user_id = "alaa_sedeeq"
# config = {
#     "recursion_limit": 30,
#     "configurable": {
#         "thread_id": thread_id,
#         "user_id": user_id
#         }
# }

# state = {
#     "messages": [],
#     "sessions": [],
#     "latest_module": TrainingModuleState(
#         name="impromptu",
#         data=ImpromptuData(
#             topic="Ethics and Philosophy",
#             topic_title="",
#             user_transcript_validation=ImpromptuValidationResponse(
#                 is_valid=False, invalid_reasons=[], followup_message=""
#                 ),
#             user_transcript_evaluation=ImpromptuEvaluation(
#                 structure=ImpromptuStructureEvaluationResponse(
#                     score=1, has_intro=False,
#                     has_conclusion=False,
#                     organization="chaotic",
#                     key_strength="",
#                     to_improve=""
#                     ),
#                 fluency=ImpromptuFluencyEvaluationResponse(
#                   filler_words=0,
#                   clarity="mumbled",
#                   fluency_score=1
#                   ),
#                 feedback=""
#             )
#     )
#     )
#     }

# state = impromptu_graph.invoke(state, config)

# state["messages"] = []

# state["messages"].append(HumanMessage(content="START"))
# state = impromptu_graph.invoke(state, config)

# test_transcript_1 = """
# Uh, leadership is important because... like, leaders need to guide teams.
# First, communication matters. Second, empathy. Third, decision-making.
# In conclusion, good leaders are crucial.
# """
# state["messages"].append(HumanMessage(content=test_transcript_1))
# state = impromptu_graph.invoke(state, config)

# test_transcript_2="""Okay, so... social media influencers, right? They're everywhere these days. But let's talk about the ethical side of this. Uh, first off, there's the transparency issue. Like, when someone promotes a skincare product with flawless filters, but doesn't disclose they're using Photoshop... that's misleading, you know?

# Then there's the whole... [pause] the whole targeting of vulnerable audiences. I mean, teenagers seeing constant '#ad posts about weight loss teas? That can really mess with self-esteem. But wait – who's responsible here? The influencer? The brand? Or maybe the platforms allowing this?

# I remember this one case where a influencer promoted a crypto scam. People lost thousands! That's... that's just wrong. But on the flip side, some creators are using their platforms for good – like promoting sustainability while being upfront about sponsorships.

# So ultimately, I think we need clearer ethical guidelines. Maybe... mandatory disclosure labels? Or accountability measures? Because right now, it feels like the Wild West of advertising, and regular users are paying the price."""

# state["messages"].append(HumanMessage(content=test_transcript_2))

# state = impromptu_graph.invoke(state, config)

# print(state)

###########
### PLOT
###########
# save_graph_image(build_presentation_assessment_graph(), "presentation_assessment_graph.png")
# save_graph_image(build_impromptu_sgraph(), "impromptu_graph.png")
# save_graph_image(build_storytelling_graph(), "storytelling_graph.png")
# save_graph_image(build_conflict_resolution_graph(), "conflict_resolution_graph.png")