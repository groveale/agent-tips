import os
from autogen import AssistantAgent, UserProxyAgent
from config import get_azure_config

# Get Azure OpenAI configuration
azure_llm_config = get_azure_config()

# Create the agents with their roles
research_agent = AssistantAgent(
    name="ResearchAgent", 
    llm_config=azure_llm_config,
    system_message="""You are ResearchAgent, an AI assistant specialised in researching topics thoroughly.
Provide detailed, factual information on the given topic in a well-structured format.
Use headings and bullet points where appropriate to organise information.
Wait for your turn to speak in the conversation.
End your message with 'RESEARCH COMPLETE'."""
)

summariser_agent = AssistantAgent(
    name="SummariserAgent", 
    llm_config=azure_llm_config,
    system_message="""You are SummariserAgent, an AI assistant specialised in summarising complex information.
Take the detailed research provided by ResearchAgent and create a concise summary with 5 key points.
Wait for ResearchAgent to finish before providing your summary.
End your message with 'SUMMARY COMPLETE'."""
)

recommender_agent = AssistantAgent(
    name="RecommenderAgent", 
    llm_config=azure_llm_config,
    system_message="""You are RecommenderAgent, an AI assistant specialised in providing actionable recommendations.
Based on the information from ResearchAgent and SummariserAgent, provide 3-5 specific, practical recommendations.
Wait for SummariserAgent to finish before providing your recommendations.
End your message with 'RECOMMENDATIONS COMPLETE'."""
)

# Simple user proxy that doesn't need human input
user_proxy = UserProxyAgent(
    name="User", 
    human_input_mode="NEVER", 
    code_execution_config=False,
    system_message="You are a user who needs information on a topic."
)

def extract_agent_message(output: str, start_marker: str, end_marker: str) -> str:
    """Extract message between start and end markers"""
    try:
        start = output.split(start_marker)[1].split(":", 1)[1]
        end = start.split(end_marker)[0]
        return end.strip()
    except IndexError:
        return ""