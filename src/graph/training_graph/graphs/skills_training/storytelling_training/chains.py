from langchain.prompts import PromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

from src.graph.utils import create_chain
from .types import (
    StoryValidationResponse,
    StoryNarrativeEvaluation,
    StoryEngagementEvaluation
    )

# os.environ['GROQ_API_KEY'] = userdata.get('GROQ_API')
model_name = "llama-3.1-8b-instant"
#"llama-3.2-3b-preview" "llama-3.1-8b-instant" "llama-3.3-70b-versatile" "llama3-8b-8192"


# ======== Storytelling Chains ========
story_prompt_chain = (
    PromptTemplate.from_template(
        """Generate a story starter for {genre} genre.
Examples:
- Personal: "Write about a time you faced an unexpected challenge..."
- Fictional: "In a world where memories are currency..."
- Historical: "Describe a day in the life of a 1920s factory worker..."

Output ONLY the prompt:"""
    )
    | ChatGroq(model=model_name, temperature=0.7)
)

# Story Validation Chain
story_validation_example = {
    "is_valid": False,
    "invalid_reasons": ["too_short"],
    "followup_message": "Expand story to at least 300 words"
}

story_validation_chain = create_chain(
    """Validate story against these criteria:
1. Matches {genre} genre
2. Minimum 300 words
3. Clear beginning-middle-end
4. Logical plot progression
5. No offensive content

Story: {story}

Respond with JSON:""",
    StoryValidationResponse,
    story_validation_example,
    ChatGroq(model=model_name),
    0.3
)

# Narrative Analysis Chain
story_narrative_example = {
    "narrative_score": 7,
    "character_development": 3,
    "plot_complexity": 4,
    "literary_devices": ["metaphor", "flashback"],
    "key_strength": "Strong emotional tension",
    "to_improve": "Develop secondary characters"
}

story_narrative_analyzer = create_chain(
    """Analyze story narrative:
1. Character depth/development
2. Plot complexity
3. Literary devices used
4. Emotional arc quality

Story: {story}
Respond with JSON:""",
    StoryNarrativeEvaluation,
    story_narrative_example,
    ChatGroq(model=model_name),
    0.2
)

# Engagement Analysis Chain
story_engagement_example = {
    "engagement_score": 8,
    "hook_quality": "strong",
    "pacing_analysis": "consistent",
    "reader_interest": "high",
    "satisfaction": "adequate"
}

story_engagement_analyzer = create_chain(
    """Evaluate story engagement:
1. Opening hook impact
2. Pacing analysis
3. Reader interest maintenance
4. Ending satisfaction

Story: {story}
Respond with JSON:""",
    StoryEngagementEvaluation,
    story_engagement_example,
    ChatGroq(model=model_name),
    0.2
)

# ======== Followup Chain ========
story_followup_chain = (
    PromptTemplate.from_template(
        """Act as a communication coach. Provide SPECIFIC guidance to fix these story validation issues:

**Genre**: {genre}
**Issues Detected**: {invalid_reasons}

**Original Attempt**:
{story}

**Guidance Rules**:
1. Address ONLY the listed validation issues
2. Provide 1-2 concrete steps per issue
3. Include EXAMPLE phrases/sentences
4. Keep under 100 words
5. Never invent new issues

**Example for ["off_genre"]**:
"Let's refocus on '{genre}':
1. Replace general statements with specific examples about {genre}
(e.g., 'For instance, in {genre} situations like...')

**Your Guidance**:"""
    )
    | ChatGroq(model=model_name, temperature=0.3)
)

# Story Feedback Chain
story_feedback_chain = (
    PromptTemplate.from_template(
        """Generate writing feedback using:
Narrative: {narrative}
Engagement: {engagement}

Format:
1. Highlight strongest element
2. Suggest ONE key improvement
3. Recommend writing exercise
4. Keep under 100 words

Example:
"Your vivid characters (strength) carry the story. Deepen the setting descriptions (improvement). Practice describing locations using 3 senses (exercise)."
"""
    )
    | ChatGroq(model=model_name, temperature=0.5)
)
