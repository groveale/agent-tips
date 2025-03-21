import os

from autogen import AssistantAgent, UserProxyAgent

azure_openai_key = os.getenv("AZURE_OPENAI_API_KEY")
azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_openai_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

if not azure_openai_key or not azure_openai_endpoint or not azure_openai_deployment:
    raise ValueError("Set the environment variables. You need an API key, an endpoint and a deployment name. Check the demo documentation for details. \nMake sure you included the \"s when setting the environment variables if needed.\n")

azure_llm_config = {
    "api_key": azure_openai_key,
    "base_url": azure_openai_endpoint,
    "api_type": "azure",
    "api_version": "2025-01-01-preview",
    "model": azure_openai_deployment 
}

# Define system messages for each agent - you can modify this part to experiment with the agent behaviour
research_system_message = """You are ResearchAgent, an AI assistant specialised in researching topics thoroughly.
Provide detailed, factual information on the given topic in a well-structured format.
Use headings and bullet points where appropriate to organise information.
Wait for your turn to speak in the conversation.
End your message with 'RESEARCH COMPLETE'."""

summariser_system_message = """You are SummariserAgent, an AI assistant specialised in summarising complex information.
Take the detailed research provided by ResearchAgent and create a concise summary with 5 key points.
Wait for ResearchAgent to finish before providing your summary.
End your message with 'SUMMARY COMPLETE'."""

recommender_system_message = """You are RecommenderAgent, an AI assistant specialised in providing actionable recommendations.
Based on the information from ResearchAgent and SummariserAgent, provide 3-5 specific, practical recommendations.
Wait for SummariserAgent to finish before providing your recommendations.
End your message with 'RECOMMENDATIONS COMPLETE'."""

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

user_proxy = UserProxyAgent(
    name="User", 
    human_input_mode="NEVER", 
    code_execution_config=False,  # Disable code execution completely
    system_message="You are a user who needs information on a topic. You initiate the conversation and only respond if directly asked a question."
)