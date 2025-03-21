import os
import io
from typing import Dict
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from contextlib import redirect_stdout

# Get Azure OpenAI configuration from environment variables
azure_openai_key = os.getenv("AZURE_OPENAI_API_KEY")
azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_openai_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

if not azure_openai_key or not azure_openai_endpoint or not azure_openai_deployment:
    raise ValueError("Azure OpenAI environment variables are not set. Check the demo documentation for details.")

azure_llm_config = {
    "api_key": azure_openai_key,
    "base_url": azure_openai_endpoint,
    "api_type": "azure",
    "api_version": "2025-01-01-preview",
    "model": azure_openai_deployment 
}

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

user_proxy = UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    code_execution_config=False,
    system_message="You are a user who needs information on a topic."
)

def extract_agent_message(output: str, start_marker: str, end_marker: str) -> str:
    """Extract message between start and end markers"""
    start_idx = output.find(start_marker)
    if start_idx == -1:
        return ""
    
    # Find the actual start of the message content
    start_idx = output.find(":", start_idx)
    if start_idx == -1:
        return ""
    start_idx += 1
    
    end_idx = output.find(end_marker, start_idx)
    if end_idx == -1:
        return output[start_idx:].strip()
        
    return output[start_idx:end_idx + len(end_marker)].strip()

def run_agents(user_query: str) -> Dict[str, str]:
    """Run the multi-agent conversation and return the messages for each agent"""
    output = io.StringIO()
    
    with redirect_stdout(output):
        # Set up the group chat with all agents
        agents = [research_agent, summariser_agent, recommender_agent, user_proxy]
        group_chat = GroupChat(agents=agents, messages=[], max_round=4)
        manager = GroupChatManager(groupchat=group_chat, llm_config=research_agent.llm_config)

        # Start the conversation
        user_proxy.initiate_chat(
            manager,
            message=f"""
I need a comprehensive answer to the following question: {user_query}

This conversation will follow a strict sequence:
1. ResearchAgent: Provide detailed research on this topic.
2. SummariserAgent: After ResearchAgent finishes, summarise the key points.
3. RecommenderAgent: After SummariserAgent finishes, provide practical recommendations.

@ResearchAgent, please begin with your detailed research on this topic.
            """
        )
    
    # Extract and return messages from the conversation
    conversation_log = output.getvalue()
    
    return {
        "research": extract_agent_message(conversation_log, "ResearchAgent (to chat_manager)", "RESEARCH COMPLETE"),
        "summary": extract_agent_message(conversation_log, "SummariserAgent (to chat_manager)", "SUMMARY COMPLETE"),
        "recommendations": extract_agent_message(conversation_log, "RecommenderAgent (to chat_manager)", "RECOMMENDATIONS COMPLETE")
    }