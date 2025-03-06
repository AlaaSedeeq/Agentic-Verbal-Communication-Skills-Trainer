STRUCTURE_PROMPT = """Analyze presentation structure:
{script}

Evaluate (1-5 scores):
- Introduction clarity
- Conclusion effectiveness
- Transition smoothness

Format JSON with: intro_score, conclusion_score, transition_score, structure_comment"""

DELIVERY_PROMPT = """Analyze speaking delivery from this script:
{script}

Return JSON with these fields:
- pacing_score: 1-5 rating (1=too slow, 5=ideal)
- clarity_score: 1-5 rating (1=mumbled, 5=excellent)
- filler_words: list of detected filler words
- delivery_comment: brief analysis

Example Output:
{{
  "pacing_score": 3,
  "clarity_score": 4,
  "filler_words": ["um", "like"],
  "delivery_comment": "Moderate pace with some hesitation"
}}"""

CONTENT_PROMPT = """Evaluate presentation content:
{script}

Assess:
- Relevance to topic (1-5)
- Persuasiveness (1-5)
- Vocabulary level (basic/intermediate/advanced)
- Content quality comments"""

VALIDATION_PROMPT = """Evaluate presentation script validity:
{script}

Check for:
- Minimum 200 characters
- Complete sentences
- Appropriate language
- Relevant content

Return JSON with:
- is_valid: boolean
- issues: list of problems
- correction_guidance: brief instructions for improvement"""

FEEDBACK_TEMPLATE = """Generate presentation feedback report:

Structure:
- Intro: {intro}/5 ({structure_comment})
- Conclusion: {conclusion}/5
- Transitions: {transitions}/5

Delivery:
- Pacing: {pacing}/5
- Clarity: {clarity}/5
- Filler words: {fillers}

Content:
- Relevance: {relevance}/5
- Persuasiveness: {persuasion}/5
- Vocabulary: {vocab}

Prioritize these improvements:
1. {improvement1}
2. {improvement2}

Final Score: {score}/10"""
