# Multi-Agent Research Demo

This beginner-friendly demo shows how multiple AI assistants (agents) can work together as a team to research topics for you.

## What Does This Demo Do?

When you run this demo with a question, three AI agents work together in order:

1. **ResearchAgent**: Gathers detailed information about your topic
2. **SummariserAgent**: Picks out the most important points
3. **RecommenderAgent**: Suggests practical next steps based on the research

These assistants are managed by a coordinator that makes sure they work in the right order and communicate properly.

## Before You Start

You'll need:
- Python 3.8 or newer installed on your computer
- Access to Azure OpenAI (Microsoft's AI service)
- A few Python packages (listed in the `requirements.txt` file)

## Step-by-Step Guide

### 1. Install the Required Software

Open your command prompt or terminal and type:

```bash
pip install -r requirements.txt
```

This installs all the helper software needed to run the demo.

### 2. Set Up Your AI Connection

You need to tell the program how to connect to the AI service. Replace the bits in brackets with your actual information.

#### Windows (PowerShell)

Open PowerShell and type:

```powershell
$env:AZURE_OPENAI_API_KEY="[your-openai-api-key]"
$env:AZURE_OPENAI_ENDPOINT="https://[your-resource-here].openai.azure.com/"
$env:AZURE_OPENAI_DEPLOYMENT="[your-model-deployment-name]"
```

#### Windows (Command Prompt)

```cmd
set AZURE_OPENAI_API_KEY=[your-openai-api-key]
set AZURE_OPENAI_ENDPOINT=https://[your-resource-here].openai.azure.com/
set AZURE_OPENAI_DEPLOYMENT=[your-model-deployment-name]
```

#### macOS/Linux

```bash
export AZURE_OPENAI_API_KEY=[your-openai-api-key]
export AZURE_OPENAI_ENDPOINT=https://[your-resource-here].openai.azure.com/
export AZURE_OPENAI_DEPLOYMENT=[your-model-deployment-name]
```

### 3. Run the Demo

From the main folder of the project, type:

```bash
python demos/multi-agent-research/cli.py "Explain multi-agent orchestration."
```

You can change the text in quotes to any question you want to research!

## How Does It Work?

1. You ask a question
2. Your question goes to the AI 'team manager'
3. The Research Agent studies your topic in detail
4. The Summariser Agent creates a simple summary of the important points
5. The Recommender Agent suggests practical next steps
6. All results appear on your screen

## What You'll See

```
Starting multi-agent conversation to answer your query. Please wait...

--- TASK COMPLETE ---

### CONVERSATION SUMMARY ###

ResearchAgent:
[Detailed research on the topic]
RESEARCH COMPLETE

--------------------------------------------------------------------------------

SummariserAgent:
[Summary of key points]
SUMMARY COMPLETE

--------------------------------------------------------------------------------

RecommenderAgent:
[Practical recommendations]
RECOMMENDATIONS COMPLETE

--------------------------------------------------------------------------------

### END OF CONVERSATION ###
```

## Making Changes

If you want to change how the agents behave, you can edit their instructions in the `agents.py` file.

## Fixing Common Problems

- **Connection Settings**: Make sure you've entered your Azure settings correctly, including the quote marks
- **API Access**: Check that your Azure OpenAI key can access the AI model you specified
- **Results Quality**: The quality of answers depends on which AI model you're using in Azure

## Technical Details

For developers and technical users interested in the underlying architecture:

### System Architecture

This demo implements a multi-agent system using AutoGen, a framework for building agent-based applications. The architecture follows these key components:

1. **Agent Definitions** (`agents.py`): 
   - Three `AssistantAgent` instances with specialized system prompts
   - One `UserProxyAgent` that serves as the interface between user and agents
   - Azure OpenAI configuration for API connections

2. **Orchestration** (`cli.py`):
   - `GroupChat` class manages the conversation between multiple agents
   - `GroupChatManager` coordinates turn-taking and conversation flow
   - Sequential processing pattern enforced by system prompts and conversation design

3. **Conversation Flow**:
   - User query is initiated through the `UserProxyAgent.initiate_chat()` method
   - `GroupChatManager` uses an LLM to decide which agent should speak next
   - Agents respond in sequence based on their specialized roles
   - Maximum conversation rounds limited to 6 to ensure completion

### Agent System Prompts

Each agent has a carefully crafted system prompt that defines its role:

- **ResearchAgent**: Instructed to provide detailed research without attempting to access external resources
- **SummariserAgent**: Waits for ResearchAgent to finish, then extracts exactly 5 key points
- **RecommenderAgent**: Waits for both previous agents to complete, then provides 3-5 specific recommendations

### Technical Constraints

- **Input Handling**: `UserProxyAgent` is configured with `human_input_mode="NEVER"` to automate the conversation
- **Code Execution**: Disabled via `code_execution_config=False` for security
- **Conversation Control**: Uses completion markers (e.g., "RESEARCH COMPLETE") to signal agent task completion
- **LLM Configuration**: Uses Azure OpenAI API with configurable model deployment

This implementation demonstrates how to build a coordinated multi-agent system with clear role separation and sequential processing, all orchestrated through a central group chat manager.