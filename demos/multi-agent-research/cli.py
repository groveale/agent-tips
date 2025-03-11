import argparse
from agents import user_proxy, research_agent, summariser_agent, recommender_agent
from autogen import GroupChat, GroupChatManager

def run_demo(user_query):
    agents = [research_agent, summariser_agent, recommender_agent, user_proxy]
    
    group_chat = GroupChat(
        agents=agents,
        messages=[],
        max_round=6
    )
    
    manager = GroupChatManager(
        groupchat=group_chat, 
        llm_config=research_agent.llm_config
    )

    print("\nStarting multi-agent conversation to answer your query. Please wait...")
    
    user_proxy.initiate_chat(
        manager,
        message=f"""
I need a comprehensive answer to the following question: {user_query}

This conversation will follow a strict sequence:
1. ResearchAgent: Provide detailed research on this topic.
2. SummariserAgent: After ResearchAgent finishes, summarize the key points.
3. RecommenderAgent: After SummariserAgent finishes, provide practical recommendations.

@ResearchAgent, please begin with your detailed research on this topic.
        """
    )

    messages = group_chat.messages
    
    print("\n--- TASK COMPLETE ---\n")
    print("### CONVERSATION SUMMARY ###\n")
    
    # Filter out system messages and focus on agent responses
    agent_messages = []
    for message in messages:
        if message.get("content") and message.get("name") in ["ResearchAgent", "SummariserAgent", "RecommenderAgent", "User"]:
            agent_messages.append(message)
    
    for message in agent_messages:
        sender = message["name"]
        content = message["content"]
        print(f"\n{sender}:\n{content}\n")
        print("-" * 80)
    
    print("\n### END OF CONVERSATION ###")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-Agent AI CLI")
    parser.add_argument("query", type=str, help="Enter your question for the AI agents to research!")
    args = parser.parse_args()
    run_demo(args.query)