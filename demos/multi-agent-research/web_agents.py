import io
from typing import Dict
from autogen import GroupChat, GroupChatManager
from agents import research_agent, summariser_agent, recommender_agent, user_proxy, extract_agent_message

def run_agents(user_query: str) -> Dict[str, str]:
    """Run the multi-agent conversation and return the messages for each agent"""
    output = io.StringIO()
    
    with redirect_stdout(output):
        agents = [research_agent, summariser_agent, recommender_agent, user_proxy]
        group_chat = GroupChat(agents=agents, messages=[], max_round=4)
        manager = GroupChatManager(groupchat=group_chat, llm_config=research_agent.llm_config)

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
    
    conversation_log = output.getvalue()
    
    # Extract messages from each agent
    research = extract_agent_message(conversation_log, "ResearchAgent (to chat_manager)", "RESEARCH COMPLETE")
    summary = extract_agent_message(conversation_log, "SummariserAgent (to chat_manager)", "SUMMARY COMPLETE")
    recommendations = extract_agent_message(conversation_log, "RecommenderAgent (to chat_manager)", "RECOMMENDATIONS COMPLETE")
    
    return {
        "research": research,
        "summary": summary,
        "recommendations": recommendations
    }