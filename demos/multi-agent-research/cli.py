import argparse
from agents import user_proxy, research_agent, summariser_agent, recommender_agent
from autogen import GroupChat, GroupChatManager

def run_demo(user_query: str) -> None:
    """Run the multi-agent research demo with the given query"""
    agents = [research_agent, summariser_agent, recommender_agent, user_proxy]
    group_chat = GroupChat(agents=agents, messages=[], max_round=4)
    manager = GroupChatManager(groupchat=group_chat, llm_config=research_agent.llm_config)

    print("\nStarting multi-agent conversation to answer your query. Please wait...\n")
    
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Multi-Agent Research System - Get comprehensive research on any topic!"
    )
    parser.add_argument(
        "query", 
        type=str, 
        help="Your research question"
    )
    args = parser.parse_args()
    run_demo(args.query)