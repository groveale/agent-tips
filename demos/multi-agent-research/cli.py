import argparse
from tasks import process_research_query


def run_demo(user_query: str) -> None:
    """Run the multi-agent research demo with the given query"""
    print("\nStarting multi-agent conversation to help you learn. "
          "Please wait...\n")
    results = process_research_query(user_query)
    print("\n--- TASK COMPLETE ---\n")
    print("### CONVERSATION SUMMARY ###\n")
    print("ResearchAgent:")
    print(results["research"])
    print("\n" + "-" * 80 + "\n")
    print("FlashcardAgent:")
    print(results["flashcards"])
    print("\n" + "-" * 80 + "\n")
    print("NextStepsAgent:")
    print(results["next_steps"])
    print("\n" + "-" * 80 + "\n")
    print("### END OF CONVERSATION ###")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Study Assistant - Get comprehensive study materials on any topic!"
        )
    )
    parser.add_argument(
        "query",
        type=str,
        help="The topic you want to learn about"
    )
    args = parser.parse_args()
    run_demo(args.query)
