from autogen import AssistantAgent, UserProxyAgent
from config import get_azure_config


# Message markers as constants
RESEARCH_END = "RESEARCH COMPLETE"
FLASHCARDS_END = "FLASHCARDS COMPLETE"
NEXT_STEPS_END = "NEXT STEPS COMPLETE"

# Get Azure OpenAI configuration
azure_llm_config = get_azure_config()


def create_agent_team():
    """Create and return the team of agents"""
    research_agent = AssistantAgent(
        name="ResearchAgent",
        llm_config=azure_llm_config,
        system_message=(
            "You are ResearchAgent, an AI assistant specialised in "
            "researching topics thoroughly.\n"
            "Provide detailed, factual information on the given topic in a "
            "well-structured format.\n"
            "Use headings and bullet points where appropriate to organise "
            "information.\n"
            f"End your message with '{RESEARCH_END}'."
        )
    )

    flashcard_agent = AssistantAgent(
        name="FlashcardAgent",
        llm_config=azure_llm_config,
        system_message=(
            "You are FlashcardAgent, an AI assistant specialised in "
            "creating effective study flashcards.\n"
            "Take the detailed research provided by ResearchAgent and "
            "create 5-8 high-quality flashcards.\n"
            "Each flashcard should follow this format:\n"
            "Q: [Clear, specific question about a key concept]\n"
            "A: [Concise, accurate answer]\n\n"
            "Focus on core concepts, definitions, and relationships.\n"
            f"End your message with '{FLASHCARDS_END}'."
        )
    )

    next_steps_agent = AssistantAgent(
        name="NextStepsAgent",
        llm_config=azure_llm_config,
        system_message=(
            "You are NextStepsAgent, an AI assistant specialised in "
            "suggesting study paths and strategies.\n"
            "Based on the research and flashcards provided, suggest "
            "ways to study and master the subject matter.\n"
            "Include:\n"
            "1. Recommended learning sequence\n"
            "2. Practical exercises or projects\n"
            "3. Additional resources (books, courses, videos)\n"
            "4. Study techniques specific to this topic\n\n"
            f"End your message with '{NEXT_STEPS_END}'."
        )
    )

    # Simple user proxy that doesn't need human input
    user_proxy = UserProxyAgent(
        name="User",
        human_input_mode="NEVER",
        code_execution_config=False,
        system_message="You are a user who needs information on a topic."
    )

    agent_dict = {
        "research_agent": research_agent,
        "flashcard_agent": flashcard_agent,
        "next_steps_agent": next_steps_agent,
        "user_proxy": user_proxy
    }

    agent_list = [
        research_agent,
        flashcard_agent,
        next_steps_agent,
        user_proxy
    ]

    return agent_dict, agent_list
