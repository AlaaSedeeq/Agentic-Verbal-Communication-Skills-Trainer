# Scenario Generation Chain
conflict_scenario_prompt = """Generate a conflict scenario about {category}.
Examples:
- "Your teammate missed a deadline affecting your project"
- "A client is upset about delayed deliverables"
- "A colleague takes credit for your work"

Output ONLY the scenario:"""

# Response Validation Chain
conflict_validation_example = {
    "is_valid": False,
    "invalid_reasons": ["aggressive"],
    "followup_message": "Avoid accusatory language like 'you always'"
}

conflict_validation_prompt = """Validate conflict response STRICTLY. Respond ONLY with JSON:

Validation Criteria:
1. Check for aggression (words like 'you always', 'your fault')
2. Detect avoidance ('not my problem', 'don't care')
3. Verify relevance to scenario
4. Minimum 50 words

Formatting Rules:
- NO explanations
- NO code blocks
- ONLY valid JSON

Example Response:
{{"is_valid": false, "invalid_reasons": ["aggressive"], "followup_message": "Avoid 'you' statements"}}

Category: {category}
Scenario: {scenario}
Response: {response}

JSON:"""

# Diplomacy Evaluation Chain
conflict_diplomacy_evaluation_example = {
    "empathy_score": 4,
    "clarity_score": 3,
    "solution_focus": 5,
    "professionalism": "excellent",
    "negative_indicators": []
}

conflict_diplomacy_evaluation_prompt = """Evaluate diplomatic response. Return ONLY JSON:

Evaluation Criteria:
1. Empathy (1-5): Acknowledgement of others' perspectives
2. Clarity (1-5): Directness without aggression
3. Solution Focus (1-5): Concrete suggestions
4. Professionalism: Appropriate tone
5. Negative Indicators: Any hostile language

Response Format:
{
  "empathy_score": 4,
  "clarity_score": 3,
  "solution_focus": 5,
  "professionalism": "excellent",
  "negative_indicators": []
}

Scenario: {scenario}
Response: {response}

JSON:"""


# Feedback Chain
conflict_feedback_prompt = """Generate diplomatic feedback using:
{diplomacy}

Format:
1. Highlight strongest diplomatic skill
2. Identify ONE key improvement
3. Suggest role-play exercise
4. Keep under 100 words

Example:
"Great empathy in acknowledging feelings (strength). Work on clearer action steps (improvement). Practice rephrasing 'You' statements as 'We' solutions."
"""