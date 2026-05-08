"""
Main application file to run the multi-agent system for cartoonization.
"""
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

from agents.project_manager import ProjectManager
from agents.image_analyzer import ImageAnalyzer
from agents.art_director import ArtDirector
from agents.qa_critic import QACritic

# Define the state for the graph
class WorkflowState(TypedDict):
    image_path: str
    style_prompt: str
    analysis: str
    generated_image: str
    feedback: dict

# Initialize agents
project_manager = ProjectManager()
image_analyzer = ImageAnalyzer()
art_director = ArtDirector()
qa_critic = QACritic()

# Define the nodes for the graph
def analyze_image_node(state):
    analysis_result = image_analyzer.analyze_image(state["image_path"])
    return {"analysis": analysis_result["analysis"]}

def generate_cartoon_node(state):
    generation_result = art_director.generate_cartoon(state)
    return {"generated_image": generation_result["generated_image"]}

def qa_critic_node(state):
    evaluation_result = qa_critic.evaluate_image(state)
    return {"feedback": evaluation_result["feedback"]}

# Define the conditional edge logic
def should_continue(state):
    if state["feedback"]["approved"]:
        return "end"
    else:
        return "regenerate"

# Build the graph
workflow = StateGraph(WorkflowState)

workflow.add_node("analyzer", analyze_image_node)
workflow.add_node("generator", generate_cartoon_node)
workflow.add_node("critic", qa_critic_node)

workflow.set_entry_point("analyzer")
workflow.add_edge("analyzer", "generator")
workflow.add_edge("generator", "critic")
workflow.add_conditional_edges(
    "critic",
    should_continue,
    {
        "end": END,
        "regenerate": "generator",
    },
)

# Compile the graph
app = workflow.compile()

# --- Main execution ---
if __name__ == "__main__":
    # This is a placeholder for user input.
    # In a real application, you would get this from a UI or command line.
    input_image_path = "/Users/floyd/Desktop/testfig.png" 
    input_style_prompt = "Classic Disney style"

    initial_state = project_manager.start_workflow(input_image_path, input_style_prompt)
    
    # Run the workflow
    final_state = app.invoke(initial_state)

    print("\n--- Workflow Complete ---")
    print(f"Final generated image: {final_state.get('generated_image')}")
    print(f"Final feedback: {final_state.get('feedback')}")
