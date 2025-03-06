import gradio as gr
from datetime import datetime

from src.common.config import load_config
from .db_manager import DatabaseManager

# Simulated AI Feedback (to be replaced with actual LLM)
class AIFeedbackGenerator:
    @staticmethod
    def generate_feedback(module, user_input):
        """
        Simulate AI feedback generation.
        In a real implementation, this would call an actual LLM API.
        """
        # Basic scoring and feedback logic
        structure_score = min(max(len(user_input.split()) / 20, 1), 5)
        fluency_score = min(max(len(set(user_input.split())) / 10, 1), 5)
        
        feedback_templates = {
            "impromptu": [
                "Good start! Consider adding more specific examples.",
                "Try to provide a more structured argument with clear points.",
                "Your response shows potential. Work on clarity and conciseness."
            ],
            "conflict": [
                "Diplomatic approach. Could be more empathetic.",
                "Consider using more active listening techniques.",
                "Good attempt at resolving the conflict constructively."
            ],
            "storytelling": [
                "Interesting narrative. Focus on creating more vivid descriptions.",
                "Good story structure. Work on building emotional connection.",
                "Try to add more sensory details to engage the listener."
            ]
        }
        
        return {
            "structure": round(structure_score, 1),
            "fluency": round(fluency_score, 1),
            "feedback": feedback_templates.get(module, 
                ["Generic feedback. Specific module feedback not found."])[0],
            "timestamp": datetime.now().isoformat()
        }

# Main Application
class CommunicationSkillsTrainer:
    def __init__(self):
        self.config_manager = load_config().app.graphs.skills_training.topic_categories
        self.db_manager = DatabaseManager()
        self.ai_feedback = AIFeedbackGenerator()
        
    def create_interface(self):
        with gr.Blocks(title="Communication Skills Trainer", theme=gr.themes.Soft()) as app:
            # State Management
            current_user = gr.State(value=None)
            latest_module = gr.State(value=None)
            current_submodule = gr.State(value=None)
            
            # Login and Registration Section
            with gr.Tab("Login"):
                with gr.Column():
                    login_username = gr.Textbox(label="Username")
                    login_password = gr.Textbox(label="Password", type="password")
                    login_btn = gr.Button("Login")
                    login_output = gr.Textbox(label="Login Status", interactive=False)
            
            with gr.Tab("Register"):
                with gr.Column():
                    reg_username = gr.Textbox(label="Choose Username")
                    reg_password = gr.Textbox(label="Choose Password", type="password")
                    reg_btn = gr.Button("Register")
                    reg_output = gr.Textbox(label="Registration Status", interactive=False)
            
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
            
            # Chat Interface
            with gr.Column(visible=False) as chat_interface:
                # Dynamic input sections
                with gr.Tabs() as input_tabs:
                    with gr.TabItem("Text Input", id="text_input"):
                        # Impromptu Speaking
                        with gr.Column(visible=False) as impromptu_inputs:
                            impromptu_topic = gr.Dropdown(
                                label="Select Topic",
                                choices=self.config_manager.impromptu_categories
                            )
                            impromptu_response = gr.Textbox(label="Your Response", lines=5)
                        
                        # Storytelling
                        with gr.Column(visible=False) as storytelling_inputs:
                            storytelling_prompt = gr.Dropdown(
                                label="Select Story Prompt",
                                choices=self.config_manager.story_categories
                            )
                            storytelling_response = gr.Textbox(label="Your Story", lines=5)
                        
                        # Conflict Resolution
                        with gr.Column(visible=False) as conflict_inputs:
                            conflict_scenario = gr.Dropdown(
                                label="Select Scenario",
                                choices=self.config_manager.conflict_categories
                            )
                            conflict_response = gr.Textbox(label="Your Response", lines=5)
                        
                        # Presentation Assessment
                        with gr.Column(visible=False) as presentation_inputs:
                            script_input = gr.Textbox(label="Paste Your Script", lines=5)
                    
                    with gr.TabItem("Audio Input", id="audio_input"):
                        audio_input = gr.Audio(sources=["microphone", "upload"], label="Upload Audio")
                
                # Submit and Feedback
                submit_btn = gr.Button("Submit")
                feedback_display = gr.JSON(label="Performance Analysis")
                chat_history = gr.Chatbot(label="Training Session", height=300)
            
            # Progress Tracking
            with gr.Column(visible=False) as progress_display:
                progress_output = gr.JSON(label="Your Progress")
            
            # Login Handlers
            def handle_login(username, password):
                if self.db_manager.authenticate(username, password):
                    return {
                        login_output: "Login Successful!",
                        module_selector: gr.Column(visible=True),
                        current_user: username
                    }
                return {
                    login_output: "Invalid Credentials",
                    current_user: None
                }
            
            def handle_registration(username, password):
                if not username or not password:
                    return {"reg_output": "Username and password cannot be empty"}
                
                if self.db_manager.register_user(username, password):
                    return {"reg_output": "Registration Successful!"}
                return {"reg_output": "Username already exists"}
            
            # Module Selection Handlers
            def handle_module_selection(module):
                if module == "Skill Training Activities":
                    return {
                        skill_submodules: gr.Column(visible=True),
                        module_selector: gr.Column(visible=False),
                        latest_module: module
                    }
                return {
                    chat_interface: gr.Column(visible=True),
                    presentation_inputs: gr.Column(visible=True),
                    latest_module: module
                }
            
            def handle_submodule_selection(submodule):
                # Map submodules to their respective inputs and states
                module_map = {
                    "Impromptu Speaking": {
                        "inputs": impromptu_inputs,
                        "module": "impromptu",
                        "active_input": impromptu_response
                    },
                    "Storytelling": {
                        "inputs": storytelling_inputs,
                        "module": "storytelling",
                        "active_input": storytelling_response
                    },
                    "Conflict Resolution": {
                        "inputs": conflict_inputs,
                        "module": "conflict",
                        "active_input": conflict_response
                    }
                }
                
                selected = module_map.get(submodule, {})
                return {
                    skill_submodules: gr.Column(visible=False),
                    chat_interface: gr.Column(visible=True),
                    impromptu_inputs: gr.Column(visible=False),
                    storytelling_inputs: gr.Column(visible=False),
                    conflict_inputs: gr.Column(visible=False),
                    selected["inputs"]: gr.Column(visible=True),
                    current_submodule: selected.get("module")
                }
            
            # Submission Handler
            def handle_submission(module, user_input, chat_history):
                # Generate AI feedback
                feedback = self.ai_feedback.generate_feedback(module, user_input)
                
                # Save progress for the user
                self.db_manager.save_progress(
                    current_user.value, 
                    module, 
                    feedback['structure']
                )
                
                # Update chat history with feedback
                updated_history = chat_history + [
                    (user_input, f"""
                    **Structure Score**: {feedback['structure']}/5.0
                    **Fluency Score**: {feedback['fluency']}/5.0
                    **Feedback**: {feedback['feedback']}
                    """)
                ]
                
                return updated_history, feedback
            
            # Progress Display
            def show_progress(username):
                return self.db_manager.get_user_progress(username)
            
            # Wire up event handlers
            login_btn.click(
                handle_login, 
                inputs=[login_username, login_password],
                outputs=[login_output, module_selector, current_user]
            )
            
            reg_btn.click(
                handle_registration,
                inputs=[reg_username, reg_password],
                outputs=[reg_output]
            )
            
            confirm_module.click(
                handle_module_selection,
                inputs=[module_choice],
                outputs=[skill_submodules, module_selector, chat_interface, 
                         presentation_inputs, latest_module]
            )
            
            start_training.click(
                handle_submodule_selection,
                inputs=[submodule_choice],
                outputs=[skill_submodules, chat_interface, 
                         impromptu_inputs, storytelling_inputs, 
                         conflict_inputs, current_submodule]
            )
            
            submit_btn.click(
                handle_submission,
                inputs=[current_submodule, impromptu_response, chat_history],
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