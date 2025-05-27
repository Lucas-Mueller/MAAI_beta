from agents import Agent, Runner, ModelSettings, HandoffInputData, handoff
import asyncio
from agents.extensions.models.litellm_model import LitellmModel
import os
from dotenv import load_dotenv
from agents_configs import (
    SKILL_FIT_AGENT_DESCRIPTION,
    CULTURAL_FIT_AGENT_DESCRIPTION, 
    MAIN_AGENT_DESCRIPTION,
    JOB_EXAMPLE,
    CV_EXAMPLE
)

load_dotenv()

from agents.mcp import MCPServer
from mcp_servers import mcp_arxiv, mcp_zotero, mcp_brave

model = "gpt-4.1"

# Define agents
main_agent = Agent(
    model=model,
    name="Main Agent",
    instructions=MAIN_AGENT_DESCRIPTION,
    mcp_servers=[mcp_arxiv, mcp_zotero, mcp_brave],
)

cultural_fit_agent = Agent(
    model=model,
    name="Cultural Fit Agent",
    instructions=CULTURAL_FIT_AGENT_DESCRIPTION,
)

skill_fit_agent = Agent(
    model=model,
    name="Skill Fit Agent",
    instructions=SKILL_FIT_AGENT_DESCRIPTION,
    mcp_servers=[mcp_brave],
)

# Set up handoff chain
main_agent.handoffs = [skill_fit_agent, cultural_fit_agent]
skill_fit_agent.handoffs = [main_agent]
cultural_fit_agent.handoffs = [main_agent]

async def main():
    try:
        async with mcp_zotero, mcp_arxiv, mcp_brave:
            result = Runner.run_streamed(
                main_agent,
                input=f"Please evaluate this candidate:\n\nCV:\n{CV_EXAMPLE}\n\nJob Description:\n{JOB_EXAMPLE}",
                max_turns=10
            )
            
            print("Starting evaluation process...\n")
            
            async for event in result.stream_events():
                if event.type == "run_item_stream_event" and event.item.type == "handoff_output_item":
                    print(f"🔄 {event.item.source_agent.name} → {event.item.target_agent.name}")
            
            print("\n=== FINAL RESULT ===")
            print(result.final_output)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())