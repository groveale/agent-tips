import os


def get_azure_config():
    """Get Azure OpenAI configuration from environment variables"""
    azure_openai_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_openai_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

    required_vars = [
        azure_openai_key,
        azure_openai_endpoint,
        azure_openai_deployment
    ]
    if not all(required_vars):
        raise ValueError(
            "Azure OpenAI environment variables are not set. "
            "Check the demo documentation for details."
        )

    return {
        "api_key": azure_openai_key,
        "base_url": azure_openai_endpoint,
        "api_type": "azure",
        "api_version": "2025-01-01-preview",
        "model": azure_openai_deployment
    }
