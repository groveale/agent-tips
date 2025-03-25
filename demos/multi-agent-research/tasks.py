import io
from contextlib import redirect_stdout
from typing import Dict
from autogen import GroupChat, GroupChatManager
from agents import (
    create_agent_team,
    RESEARCH_END,
    FLASHCARDS_END,
    NEXT_STEPS_END
)


def extract_agent_message(
    output: str,
    start_marker: str,
    end_marker: str
) -> str:
    """Extract message between start and end markers"""
    try:
        start = output.split(start_marker)[1].split(":", 1)[1]
        end = start.split(end_marker)[0]
        return end.strip()
    except IndexError:
        return ""


def process_research_query(user_query: str) -> Dict[str, str]:
    """Process a research query using the agent team and return structured
    results"""
    output = io.StringIO()

    with redirect_stdout(output):
        # Create the agent team
        agent_dict, agents = create_agent_team()

        # Set up the group chat
        group_chat = GroupChat(agents=agents, messages=[], max_round=4)
        manager = GroupChatManager(
            groupchat=group_chat,
            llm_config=agent_dict["research_agent"].llm_config
        )

        # Initiate the conversation
        message = (
            f"I need to learn about the following topic: {user_query}\n\n"
            "This conversation will follow a strict sequence:\n"
            "1. ResearchAgent: Provide detailed research on this topic.\n"
            "2. FlashcardAgent: After ResearchAgent finishes, create study "
            "flashcards from the research.\n"
            "3. NextStepsAgent: After FlashcardAgent finishes, suggest ways "
            "to study and master this topic.\n\n"
            "@ResearchAgent, please begin with your detailed research."
        )
        agent_dict["user_proxy"].initiate_chat(manager, message=message)

    conversation_log = output.getvalue()

    # Extract messages from each agent
    research = extract_agent_message(
        conversation_log,
        "ResearchAgent (to chat_manager)",
        RESEARCH_END
    )
    flashcards = extract_agent_message(
        conversation_log,
        "FlashcardAgent (to chat_manager)",
        FLASHCARDS_END
    )
    next_steps = extract_agent_message(
        conversation_log,
        "NextStepsAgent (to chat_manager)",
        NEXT_STEPS_END
    )

    return {
        "research": research,
        "flashcards": flashcards,
        "next_steps": next_steps
    }
