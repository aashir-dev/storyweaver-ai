# agents/idea_generator_agent.py
import os
import asyncio
from typing import Dict, Any

from openai import AzureOpenAI, OpenAI
from utils.prompts import IDEA_GENERATOR_PROMPT_TEMPLATE

class IdeaGeneratorAgent:
    """Agent responsible for generating creative story ideas."""
    
    def __init__(self):
        """Initialize the IdeaGeneratorAgent with OpenAI client."""
        # Get OpenAI configuration from environment
        self.api_type = os.getenv("OPENAI_API_TYPE", "openai")
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o")
        
        # Azure-specific configuration
        self.api_base = os.getenv("OPENAI_API_BASE")
        self.api_version = os.getenv("OPENAI_API_VERSION")
        self.deployment_name = os.getenv("OPENAI_DEPLOYMENT_NAME")
        
        # Initialize the appropriate client
        if self.api_type.lower() == "azure":
            if not (self.api_base and self.api_version and self.deployment_name):
                raise RuntimeError("Missing Azure OpenAI configuration in .env")
            self.client = AzureOpenAI(
                api_key=self.api_key,
                api_version=self.api_version,
                azure_endpoint=self.api_base,
            )
        else:
            self.client = OpenAI(api_key=self.api_key)
    
    def generate_idea_sync(self, prompt: str) -> Dict[str, Any]:
        """Generate creative story ideas from a user prompt (synchronous version).
        
        Args:
            prompt: User input to inspire story ideas
            
        Returns:
            Dictionary containing generated story ideas
        """
        # Format the prompt using the template
        formatted_prompt = IDEA_GENERATOR_PROMPT_TEMPLATE.format(user_input=prompt)
        
        # Make the API call
        try:
            if self.api_type.lower() == "azure":
                response = self.client.chat.completions.create(
                    model=str(self.deployment_name),
                    messages=[{"role": "user", "content": formatted_prompt}],
                    max_tokens=800,
                    temperature=0.9,  # Higher temperature for more creativity
                )
            else:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": formatted_prompt}],
                    max_tokens=800,
                    temperature=0.9,  # Higher temperature for more creativity
                )
            
            # Extract the generated ideas
            content = response.choices[0].message.content
            ideas = content.strip() if content else ""
            
            # Return the ideas in the expected format for LangGraph state
            return {"ideas": ideas}
            
        except Exception as e:
            print(f"Error generating ideas: {e}")
            return {"ideas": f"Error generating ideas: {str(e)}"}
    
    async def generate_idea(self, prompt: str) -> Dict[str, Any]:
        """Generate creative story ideas from a user prompt.
        
        Args:
            prompt: User input to inspire story ideas
            
        Returns:
            Dictionary containing generated story ideas
        """
        # Format the prompt using the template
        formatted_prompt = IDEA_GENERATOR_PROMPT_TEMPLATE.format(user_input=prompt)
        
        # Make the API call
        try:
            if self.api_type.lower() == "azure":
                response = self.client.chat.completions.create(
                    model=str(self.deployment_name),
                    messages=[{"role": "user", "content": formatted_prompt}],
                    max_tokens=800,
                    temperature=0.9,  # Higher temperature for more creativity
                )
            else:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": formatted_prompt}],
                    max_tokens=800,
                    temperature=0.9,  # Higher temperature for more creativity
                )
            
            # Extract the generated ideas
            content = response.choices[0].message.content
            ideas = content.strip() if content else ""
            
            # Return the ideas in the expected format for LangGraph state
            return {"ideas": ideas}
            
        except Exception as e:
            print(f"Error generating ideas: {e}")
            return {"ideas": f"Error generating ideas: {str(e)}"}

# Function to be used as a LangGraph node (synchronous version)
def ideaAgentNode(state: Dict[str, Any]) -> Dict[str, Any]:
    """LangGraph node for generating story ideas (synchronous version).
    
    Args:
        state: The current state of the LangGraph workflow
        
    Returns:
        Updated state with generated ideas
    """
    # Get the user prompt from state
    user_prompt = state.get("prompt", "")
    
    # Initialize the agent
    idea_agent = IdeaGeneratorAgent()
    
    # Generate ideas (synchronous)
    ideas_result = idea_agent.generate_idea_sync(user_prompt)
    
    # Return the updated state
    return ideas_result

# Function to be used as a LangGraph node (async version)
async def ideaAgentNodeAsync(state: Dict[str, Any]) -> Dict[str, Any]:
    """LangGraph node for generating story ideas (async version).
    
    Args:
        state: The current state of the LangGraph workflow
        
    Returns:
        Updated state with generated ideas
    """
    # Get the user prompt from state
    user_prompt = state.get("prompt", "")
    
    # Initialize the agent
    idea_agent = IdeaGeneratorAgent()
    
    # Generate ideas
    ideas_result = await idea_agent.generate_idea(user_prompt)
    
    # Return the updated state
    return ideas_result