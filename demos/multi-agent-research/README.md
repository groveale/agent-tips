# Multi-Agent Research Demo

## Demo

This simple demo is made to just show how a multi-agent system might work. It uses [AutoGen](https://github.com/microsoft/autogen), an open-source framework from Microsoft for agentic AI. 

1. You ask a question
2. Your question goes to the AI 'team manager'
3. The ResearchAgent studies your topic in detail
4. The SummariserAgent creates a simple summary of the important points
5. The RecommenderAgent suggests practical next steps

As this is aimed for everyone I have included thorough step-by-step instructions below.

### Instructions

#### Requirements
1. First, you need access to Azure OpenAI. [Here are the steps to deploy a model](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/create-resource?pivots=web-portal) but please note that this is a paid resource. You need the API key, the endpoint, and the model name.
2. Install an IDE. This is where you edit your code. I recommend [Visual Studio Code](https://code.visualstudio.com/). If you do use Visual Studio Code, from within the IDE itself, please install the Python extension. If you want to continue with Python in the future I also recommend Pylance. If you need help installing extensions, [click here](https://code.visualstudio.com/docs/getstarted/extensions).
3. If you don't have Python 3.8 or newer installed please [install it here](https://www.python.org/downloads/).

#### Setting Up

##### Opening the Project
1. First, let's open the project in Visual Studio Code:
   - Start Visual Studio Code
   - Click on "File" > "Open Folder..."
   - Navigate to and select the `agent-tips` folder (the root folder of this project)
   - Click "Select Folder"

   This opens the entire project structure in VS Code's file explorer on the left side.

##### Installing Required Packages
1. Open a terminal in Visual Studio Code:
   - Press Ctrl+'
   - Or if you prefer, click on "Terminal" > "New Terminal" from the top menu

2. You should be in the root folder of the project and see a path ending with `agent-tips` in your terminal. Install packages by typing:

```bash
pip install -r demos/multi-agent-research/requirements.txt
```

##### Setting Up Environment Variables

To set up environment variables (the information that the demo uses to connect to your Azure OpenAI):

1. **Finding your Azure OpenAI key/model/endpoint:**
   - Log in to the [Azure Portal](https://portal.azure.com)
   - Find your Azure OpenAI resource
   - To get your API key: Go to "Keys and Endpoint" in the left menu
   - To get your model deployment name: Go to "Model Deployments" in the left menu

2. **Setting the variables in your terminal:**

**Windows (Using Visual Studio Code with PowerShell)**:
1. If you closed your terminal from earlier please follow Step 1 from **Installing Required Packages** above again.
2. Type these commands (replace the values in brackets with your own information):

```powershell
$env:AZURE_OPENAI_API_KEY="[your-openai-api-key]"
$env:AZURE_OPENAI_ENDPOINT="https://[your-resource-name].openai.azure.com/"
$env:AZURE_OPENAI_DEPLOYMENT="[your-model-deployment-name]"
```

Remember to keep the "s above when you copy paste your own details into it.

**Windows (Using Command Prompt)**:
1. Press Win+R to open the Run dialog
2. Type "cmd" and press Enter
3. Navigate to your agent-tips folder (the root of the project again!)
4. Type these commands (replace the values in brackets with your own information):

```cmd
set AZURE_OPENAI_API_KEY=[your-openai-api-key]
set AZURE_OPENAI_ENDPOINT=https://[your-resource-name].openai.azure.com/
set AZURE_OPENAI_DEPLOYMENT=[your-model-deployment-name]
```

**macOS/Linux**:
1. Open Terminal
2. Navigate to your agent-tips folder (the root of the project again!)
3. Type these commands:

```bash
export AZURE_OPENAI_API_KEY=[your-openai-api-key]
export AZURE_OPENAI_ENDPOINT=https://[your-resource-name].openai.azure.com/
export AZURE_OPENAI_DEPLOYMENT=[your-model-deployment-name]
```

##### Running the Demo

After setting the environment variables, run the demo from the same terminal window:

```bash
python demos/multi-agent-research/cli.py "Explain multi-agent orchestration using cats."
```

You can change the text in quotes to any question you want to research!

You should see a message like "Starting multi-agent conversation to answer your query. Please wait..." If you see an error message about "missing environment variables" or "connection errors," double-check your environment variables from earlier. If you see something like "ModuleNotFoundError," pip install command may not have worked.
 
### What You'll See

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

### Making Changes

If you want to change how the agents behave, you can edit their instructions in the `agents.py` file.

### Common Problems

If you are having problems here are a few things to check:
1. Environment variables being set correctly.  This is Step 2 above.
2. Running out of tokens, using the wrong model name, endpoint URL, or API key.
3. Not running commands from the root folder of the project can cause errors.
4. If you're not happy with the quality of the results, try changing the prompt or the type of AI model you're using