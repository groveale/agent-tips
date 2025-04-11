import os
import json
from flask import Flask, render_template, request, jsonify
import autogen

from autogen import GroupChat

api_key = os.environ.get("AZURE_OPENAI_API_KEY")
api_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
api_deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT")

if not api_key or not api_endpoint or not api_deployment:
    raise ValueError("Azure OpenAI credentials not found in environment variables.")

config_list = [
    {
        "model": api_deployment,
        "api_key": api_key,
        "base_url": api_endpoint,
        "api_version": "2023-05-15",
        "api_type": "azure"
    }
]

app = Flask(__name__)

def create_agents(study_topic):
    llm_config = {"config_list": config_list}
    
    research_agent = autogen.AssistantAgent(
        name="Research_Agent",
        system_message=f"You are a research assistant specialised in gathering in-depth information about {study_topic}. "
                      f"Your task is to research {study_topic} thoroughly and provide comprehensive information that can be used "
                      f"by other agents to create educational materials.",
        llm_config=llm_config,
    )
    
    flashcard_agent = autogen.AssistantAgent(
        name="FlashCard_Agent",
        system_message=f"You are a flashcard creator specialised in creating educational flashcards. "
                      f"Using the research information provided by the Research Agent, create a set of 5-10 flashcards "
                      f"for {study_topic}. Each flashcard should include a question and an answer. "
                      f"Format the response as a JSON array of objects with 'question' and 'answer' fields.",
        llm_config=llm_config,
    )
    
    recommendation_agent = autogen.AssistantAgent(
        name="Recommendation_Agent",
        system_message=f"You are a study guide creator who specializes in creating effective study plans. "
                      f"Using the research information provided by the Research Agent, create a comprehensive "
                      f"study guide for {study_topic}. The study guide should include key concepts, learning objectives, "
                      f"recommended resources, and a study schedule.",
        llm_config=llm_config,
    )
    
    # Be careful about changing code_execution_config to True - check the README for more information about how to do this safely.

    user_proxy = autogen.UserProxyAgent(
        name="User_Proxy",
        human_input_mode="NEVER",
        system_message="You are a proxy for the user. Your job is to help guide the conversation to ensure the user gets the information they need.",
        code_execution_config=False,
    )
    
    return research_agent, flashcard_agent, recommendation_agent, user_proxy

def run_group_chat(study_topic):
    research_agent, flashcard_agent, recommendation_agent, user_proxy = create_agents(study_topic)
    
    groupchat = GroupChat(
        agents=[user_proxy, research_agent, flashcard_agent, recommendation_agent],
        messages=[],
        max_round=4, 
    )
    
    manager = autogen.GroupChatManager(
        groupchat=groupchat,
        llm_config={"config_list": config_list},
    )
    
    user_proxy.initiate_chat(
        manager,
        message=f"I want to learn about {study_topic}. Research_Agent, please provide comprehensive information about this topic. "
                f"Then, FlashCard_Agent, please create flashcards based on the research. "
                f"Finally, Recommendation_Agent, please create a study guide based on the research.",
    )
    
    results = {
        "research": None,
        "flashcards": None,
        "study_guide": None
    }
    
    for message in groupchat.messages:
        sender_name = (
            message.get("sender", {}).get("name") or message.get("name")
        )
        content = message.get("content", "").strip()

        if not sender_name or not content or "I want to learn about" in content:
            continue

        if sender_name == "Research_Agent":
            results["research"] = content

        elif sender_name == "FlashCard_Agent":
            try:
                start_idx = content.find('[')
                end_idx = content.rfind(']')
                if start_idx != -1 and end_idx != -1:
                    flashcards_json = content[start_idx:end_idx + 1]
                    results["flashcards"] = json.loads(flashcards_json)
                else:
                    results["flashcards"] = content
            except:
                results["flashcards"] = content

        elif sender_name == "Recommendation_Agent":
            results["study_guide"] = content
    
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/study', methods=['POST'])
def study():
    data = request.json
    study_topic = data.get('topic', '')
    
    if not study_topic:
        return jsonify({"error": "No study topic provided"}), 400
    
    try:
        print(f"Starting group chat for topic: {study_topic}")
        results = run_group_chat(study_topic)
        return jsonify(results)
    except Exception as e:
        print(f"Error encountered: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))