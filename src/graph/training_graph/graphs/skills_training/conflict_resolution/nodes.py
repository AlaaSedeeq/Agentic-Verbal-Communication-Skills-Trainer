import gradio as gr
import json
import os
from datetime import datetime
import sqlite3
import random
from src.common.config import load_config


# Topic Generator (Simulated - to be replaced with actual LLM in production)
class TopicGenerator:
    @staticmethod
    def generate_topic(category, module):
        """
        Generate a specific topic based on the selected category and module.
        In a real implementation, this would use an LLM to generate more nuanced topics.
        """
        topics = {
            "Impromptu": {
                "Personal Development": [
                    "Why is continuous learning important for personal growth?",
                    "How can one develop emotional intelligence?",
                    "The importance of setting and achieving personal goals"
                ],
                "Social Issues": [
                    "Should social media be more regulated?",
                    "How can we address economic inequality?",
                    "The role of individual responsibility in social change"
                ],
                "Technology": [
                    "How is artificial intelligence changing our workplace?",
                    "The ethical implications of emerging technologies",
                    "Can technology solve global environmental challenges?"
                ],
                "Environment": [
                    "What individual actions can combat climate change?",
                    "The importance of sustainable living",
                    "How can we balance economic growth with environmental protection?"
                ],
                "Career and Work": [
                    "Is remote work the future of professional life?",
                    "The importance of soft skills in career development",
                    "How to maintain work-life balance in a competitive world"
                ]
            },
            "Storytelling": {
                "Personal Growth": [
                    "Tell a story about a moment that fundamentally changed your perspective",
                    "Describe a challenge that helped you grow as a person",
                    "Share a story of unexpected personal transformation"
                ],
                "Adventure": [
                    "Recount an unexpected journey that taught you something new",
                    "Tell a story about a time you stepped out of your comfort zone",
                    "Describe an adventure that tested your limits"
                ],
                "Cultural Experience": [
                    "Share a story of a cultural encounter that broadened your worldview",
                    "Describe a moment of cultural misunderstanding and learning",
                    "Tell a story about connecting with someone from a different background"
                ],
                "Professional Journey": [
                    "Describe a turning point in your professional career",
                    "Share a story of a professional challenge you overcame",
                    "Tell about a mentor who significantly impacted your career"
                ],
                "Overcoming Challenges": [
                    "Tell a story about a time you failed and what you learned",
                    "Describe how you overcame a seemingly insurmountable obstacle",
                    "Share a story of resilience in the face of adversity"
                ]
            },
            "Conflict": {
                "Workplace Dynamics": [
                    "Your team is divided on a critical project approach",
                    "Tensions are rising between department heads",
                    "Conflicting priorities are causing team friction"
                ],
                "Team Collaboration": [
                    "A team member is consistently underperforming",
                    "Two team members are in constant disagreement",
                    "Communication breakdown in a collaborative project"
                ],
                "Professional Relationships": [
                    "Handling a disagreement with a senior colleague",
                    "Navigating a conflict with a difficult client",
                    "Addressing professional differences respectfully"
                ],
                "Client Interactions": [
                    "Client is unsatisfied with the current project direction",
                    "Misalignment of expectations with a key client",
                    "Resolving a dispute over project deliverables"
                ],
                "Leadership Challenges": [
                    "Managing a team through a period of organizational change",
                    "Addressing performance issues with a team member",
                    "Balancing team morale during a challenging project"
                ]
            }
        }
        
        # Randomly select a topic from the specific category
        return random.choice(topics.get(module.capitalize(), {}).get(category, [
            "Default topic if category not found"
        ]))

# Main Application (updated to incorporate new requirements)
class CommunicationSkillsTrainer:
    def __init__(self):
        self.config = load_config().app.graphs.skills_training.topic_categories
        self.topic_generator = TopicGenerator()
    
    def create_interface(self):
        with gr.Blocks(title="Communication Skills Trainer", theme=gr.themes.Soft()) as app:
            # State Management
            current_user = gr.State(value=None)
            current_module = gr.State(value=None)
            current_submodule = gr.State(value=None)
            current_category = gr.State(value=None)
            generated_topic = gr.State(value=None)
            
            # Login Section (simplified for brevity)
            with gr.Column() as login_section:
                username = gr.Textbox(label="Username")
                password = gr.Textbox(label="Password", type="password")
                login_btn = gr.Button("Login")
                login_status = gr.Textbox(label="Login Status", interactive=False)
            
            # Module Selection
            with gr.Column(visible=False) as module_selector:
                gr.Markdown("## Select Your Training Module")
                module_choice = gr.Radio(
                    ["Skill Training Activities", "Presentation Assessments"],
                    label="Choose Module Type"
                )
                confirm_module = gr.Button("Continue")
            
            # Skill Training Sub-Modules
            with gr.Column(visible=False) as skill_submodules:
                gr.Markdown("### Choose Your Skill Training Activity")
                submodule_choice = gr.Dropdown(
                    ["Impromptu Speaking", "Storytelling", "Conflict Resolution"],
                    label="Select Specific Activity"
                )
                start_training = gr.Button("Start Training")
            
            # Category Selection for Skill Training
            with gr.Column(visible=False) as category_selector:
                gr.Markdown("### Select Category")
                # Impromptu Speaking Categories
                impromptu_category = gr.Dropdown(
                    choices=self.config.impromptu_categories,
                    label="Impromptu Speaking Category",
                    visible=False
                )
                # Storytelling Categories
                storytelling_category = gr.Dropdown(
                    choices=self.config.story_categories,
                    label="Storytelling Category",
                    visible=False
                )
                # Conflict Resolution Categories
                conflict_category = gr.Dropdown(
                    choices=self.config.conflict_categories,
                    label="Conflict Resolution Category",
                    visible=False
                )
                select_category_btn = gr.Button("Select Category")
            
            # Chat Interface
            with gr.Column(visible=False) as chat_interface:
                # Topic Display
                topic_display = gr.Textbox(
                    label="Generated Topic", 
                    interactive=False
                )
                
                # User Response Input
                user_response = gr.Textbox(
                    label="Your Response", 
                    lines=5
                )
                
                # Submission and Feedback
                submit_btn = gr.Button("Submit")
                feedback_display = gr.JSON(label="Performance Analysis")
                chat_history = gr.Chatbot(label="Training Session", height=300)
            
            # Event Handlers
            def handle_module_selection(module):
                if module == "Skill Training Activities":
                    return {
                        skill_submodules: gr.Column(visible=True),
                        module_selector: gr.Column(visible=False),
                        current_module: module
                    }
                return {
                    chat_interface: gr.Column(visible=True),
                    current_module: "Presentation Assessments"
                }
            
            def handle_submodule_selection(submodule):
                # Show appropriate category selector
                category_map = {
                    "Impromptu Speaking": {
                        "category_input": impromptu_category,
                        "submodule": "Impromptu"
                    },
                    "Storytelling": {
                        "category_input": storytelling_category,
                        "submodule": "Storytelling"
                    },
                    "Conflict Resolution": {
                        "category_input": conflict_category,
                        "submodule": "Conflict"
                    }
                }
                
                selected = category_map.get(submodule, {})
                
                return {
                    skill_submodules: gr.Column(visible=False),
                    category_selector: gr.Column(visible=True),
                    impromptu_category: gr.Dropdown(visible=False),
                    storytelling_category: gr.Dropdown(visible=False),
                    conflict_category: gr.Dropdown(visible=False),
                    selected.get("category_input"): gr.Dropdown(visible=True),
                    current_submodule: selected.get("submodule")
                }
            
            def handle_category_selection(category):
                # Generate topic based on selected category and submodule
                topic = self.topic_generator.generate_topic(
                    category, 
                    current_submodule.value
                )
                
                return {
                    category_selector: gr.Column(visible=False),
                    chat_interface: gr.Column(visible=True),
                    topic_display: topic,
                    generated_topic: topic,
                    current_category: category
                }
            
            def handle_submission(user_response, chat_history):
                # Simulate feedback generation
                feedback = {
                    "structure": round(random.uniform(3.0, 5.0), 1),
                    "fluency": round(random.uniform(3.0, 5.0), 1),
                    "feedback": "Good attempt! Consider adding more specific details."
                }
                
                # Update chat history
                updated_history = chat_history + [
                    (user_response, f"""
                    **Structure Score**: {feedback['structure']}/5.0
                    **Fluency Score**: {feedback['fluency']}/5.0
                    **Feedback**: {feedback['feedback']}
                    """)
                ]
                
                return updated_history, feedback
            
            # Wire up event handlers
            confirm_module.click(
                handle_module_selection,
                inputs=[module_choice],
                outputs=[skill_submodules, module_selector, chat_interface, current_module]
            )
            
            start_training.click(
                handle_submodule_selection,
                inputs=[submodule_choice],
                outputs=[
                    skill_submodules, category_selector, 
                    impromptu_category, storytelling_category, 
                    conflict_category, current_submodule
                ]
            )
            
            select_category_btn.click(
                handle_category_selection,
                inputs=[
                    impromptu_category,  # Will be active when Impromptu is selected
                    storytelling_category,  # Will be active when Storytelling is selected
                    conflict_category  # Will be active when Conflict Resolution is selected
                ],
                outputs=[
                    category_selector, chat_interface, 
                    topic_display, generated_topic, current_category
                ]
            )
            
            submit_btn.click(
                handle_submission,
                inputs=[user_response, chat_history],
                outputs=[chat_history, feedback_display]
            )
        
        return app

    def launch(self):
        app = self.create_interface()
        app.launch(share=True)

# Main execution
if __name__ == "__main__":
    trainer = CommunicationSkillsTrainer()
    trainer.launch()