# Impromptu validation
impromptu_validation_example = {
    "is_valid": False,
    "invalid_reasons": ["too_short"],
    "followup_message": "Your speech needs to be at least 50 words. Try expanding with examples."
}

impromptu_validation_prompt = """Validate speech transcript against topic "{topic}":
- **IMPORTAMT**: Check relevance (off_topic), if user's Transcript is not related to the topic, you should return is_valid False
- Minimum 50 words (too_short)
- No offensive content
- Clear thesis statement

Transcript: {transcript}
Topic: {topic}

Respond with JSON:"""

# Impromptu structure
impromptu_structure_example = {
    "score": 7,
    "has_intro": True,
    "has_conclusion": False,
    "organization": "adequate",
    "key_strength": "Clear thesis statement",
    "to_improve": "Stronger conclusion needed"
}

impromptu_structure_prompt = """Analyze speech structure:
1. Check intro/conclusion presence
2. Rate organization (chaotic/adequate/logical)
3. Identify key strength/improvement

Transcript: {transcript}
Respond with JSON:"""

# Impromptu fluency
impromptu_fluency_example = {
    "filler_words": 3,
    "clarity": "clear",
    "fluency_score": 8
}

impromptu_fluency_prompt = """Evaluate speech delivery:
- Count filler words (number)
- Assess clarity (mumbled/clear/excellent)
- Score fluency (1-10)

Transcript: {transcript}
Respond with JSON:"""

# Impromptu feedback
impromptu_feedback_prompt = """Generate a **motivative** feedback using these evaluation results. Do NOT mention any scores, just the feedback:

Structure: {structure}
Fluency: {fluency}

Format:
1. Start with ONE specific strength
2. Identify ONE key improvement
3. Suggest ONE practical exercise
4. Make it conversational, no additional words
5. Do NOT show any scores or explanations in the feedback
"""

# Impromptu topic
impromptu_topic_prompt = """Generate impromptu topic about {category}.
Examples:
- "The ethics of AI in healthcare"
- "Effective remote team management"
Output ONLY the topic:"""

# Impromptu followup
impromptu_followup_prompt = """Act as a communication coach. Provide SPECIFIC guidance to fix these validation issues:

**Topic**: {topic}
**Issues Detected**: {invalid_reasons}

**Original Attempt**:
{transcript}

**Guidance Rules**:
1. Address ONLY the listed validation issues
2. Provide 1-2 concrete steps per issue
3. Include EXAMPLE phrases/sentences
4. Keep under 75 words
5. Never invent new issues

**Example for ["off_topic"]**:
"Let's refocus on '{topic}':
1. Replace general statements with specific examples about {topic}
(e.g., 'For instance, in {topic} situations like...')
2. Remove unrelated points about leadership"

**Your Guidance**:"""