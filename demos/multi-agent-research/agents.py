import os

from autogen import AssistantAgent, UserProxyAgent

azure_openai_key = os.getenv("AZURE_OPENAI_API_KEY")
azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_openai_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

if not azure_openai_key or not azure_openai_endpoint or not azure_openai_deployment:
    raise ValueError("Set the environment variables. You need an API key, an endpoint and a deployment name. Check the demo documentation for details. \nMake sure you included the \"s when setting the environment variables.\n")

azure_llm_config = {
    "api_key": azure_openai_key,
    "base_url": azure_openai_endpoint,
    "api_type": "azure",
    "api_version": "2025-01-01-preview",
    "model": azure_openai_deployment 
}

# Define system messages for each agent
research_system_message = """You are ResearchAgent, an AI assistant specialized in researching topics thoroughly.
Your role is to provide detailed, factual information on the given topic.
Do NOT try to execute code, open web browsers, or access external resources.
Instead, use your built-in knowledge to provide comprehensive information.
Respond directly with the research information in a well-structured format with clear headings and bullet points where appropriate.
You must wait for your turn to speak in the conversation.
End your message with 'RESEARCH COMPLETE' to indicate you're done with your part."""

summariser_system_message = """You are SummariserAgent, an AI assistant specialized in summarizing complex information.
Your role is to take the detailed research provided by ResearchAgent and create a concise, clear summary.
Focus on extracting exactly 5 key points and organizing them logically.
Do NOT try to execute code or access external resources.
You must wait for ResearchAgent to finish before providing your summary.
End your message with 'SUMMARY COMPLETE' to indicate you're done with your part."""

recommender_system_message = """You are RecommenderAgent, an AI assistant specialized in providing specific, actionable recommendations.
IMPORTANT: You must speak AFTER both ResearchAgent and SummariserAgent have finished speaking.
Your role is to analyze the information provided by ResearchAgent and summarized by SummariserAgent.
Based on this information, provide 3-5 specific, practical recommendations related to the topic.
These should be clear next steps or areas for the user to explore further.
Make your recommendations numbered and specific rather than general.
Do NOT try to execute code or access external resources.
You MUST wait for SummariserAgent to finish before providing your recommendations.
End your message with 'RECOMMENDATIONS COMPLETE' to indicate you're done with your part."""

research_agent = AssistantAgent(
    name="ResearchAgent", 
    llm_config=azure_llm_config,
    system_message=research_system_message
)

summariser_agent = AssistantAgent(
    name="SummariserAgent", 
    llm_config=azure_llm_config,
    system_message=summariser_system_message
)

recommender_agent = AssistantAgent(
    name="RecommenderAgent", 
    llm_config=azure_llm_config,
    system_message=recommender_system_message
)

# This acts as an entry point for user interactions
# Configure the user proxy with termination messages and no input
user_proxy = UserProxyAgent(
    name="User", 
    human_input_mode="NEVER", 
    code_execution_config=False,  # Disable code execution completely
    system_message="You are a user who needs information on a topic. You initiate the conversation and only respond if directly asked a question."
)