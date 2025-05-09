from langgraph.graph import StateGraph, START, END

from core.agents.sequence_graph.nodes import (
    pasue_gmail_toolkit,
    start_gmail_toolkit,
    resume_gmail_toolkit,
    stop_gmail_toolkit,
    restart_gmail_toolkit,
)
from core.agents.sequence_graph.states import SequenceState
from langchain_google_genai import GoogleGenAI


# Create the State Graph
sequence_graph = StateGraph(
    name="Sequence Graph",
    description="A graph to represent the sequence of states in an agent.",
    state_schema=SequenceState,
    start=START,
    end=END,
)

# Add nodes to the graph
sequence_graph.add_node(
    name="start_gmail_toolkit",
    node=start_gmail_toolkit,
    description="Start the Gmail toolkit",
)
sequence_graph.add_node(
    name="pause_gmail_toolkit",
    node=pasue_gmail_toolkit,
    description="Pause the Gmail toolkit",
)
sequence_graph.add_node(
    name="resume_gmail_toolkit",
    node=resume_gmail_toolkit,
    description="Resume the Gmail toolkit",
)
sequence_graph.add_node(
    name="stop_gmail_toolkit",
    node=stop_gmail_toolkit,
    description="Stop the Gmail toolkit",
)
sequence_graph.add_node(
    name="restart_gmail_toolkit",
    node=restart_gmail_toolkit,
    description="Restart the Gmail toolkit",
)
sequence_graph.add_node()

# Add edges to the graph
