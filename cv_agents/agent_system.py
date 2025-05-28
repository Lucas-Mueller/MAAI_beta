from agents import Agent, Runner
import asyncio
from dotenv import load_dotenv
from .agents_configs import (
    SKILL_FIT_AGENT_DESCRIPTION,
    CULTURAL_FIT_AGENT_DESCRIPTION,
    SUMMARY_AGENT_DESCRIPTION,
    MAIN_AGENT_DESCRIPTION
)

load_dotenv()

import sys
sys.path.append('..')
from mcp_servers import mcp_arxiv, mcp_zotero, mcp_brave

model = "gpt-4.1"

# Define agents
main_agent = Agent(
    model=model,
    name="Main Agent",
    instructions=MAIN_AGENT_DESCRIPTION,
    mcp_servers=[mcp_brave],
)

cultural_fit_agent = Agent(
    model=model,
    name="Cultural Fit Agent",
    instructions=CULTURAL_FIT_AGENT_DESCRIPTION,
    mcp_servers=[mcp_brave],
)

skill_fit_agent = Agent(
    model=model,
    name="Skill Fit Agent",
    instructions=SKILL_FIT_AGENT_DESCRIPTION,
    mcp_servers=[mcp_brave],
)

summary_agent = Agent(
    model=model,
    name="Summary Agent",
    instructions=SUMMARY_AGENT_DESCRIPTION,
)

# Set up handoff chain: Main -> Skill -> Cultural -> Summary -> Main
main_agent.handoffs = [skill_fit_agent]
skill_fit_agent.handoffs = [cultural_fit_agent]
cultural_fit_agent.handoffs = [summary_agent]
summary_agent.handoffs = [main_agent]

async def evaluate_cv(job_description: str, cv_text: str) -> dict:
    """
    Evaluate a CV against a job description using the multi-agent system.
    
    Args:
        job_description: Text content of the job description
        cv_text: Text content of the CV
        
    Returns:
        Dictionary containing evaluation results with scores and assessments
    """
    try:
        async with mcp_zotero, mcp_arxiv, mcp_brave:
            result = Runner.run_streamed(
                main_agent,
                input=f"Please evaluate this candidate:\n\nCV:\n{cv_text}\n\nJob Description:\n{job_description}",
                max_turns=10
            )
            
            # Wait for completion
            async for event in result.stream_events():
                pass  # Process events if needed for monitoring
            
            # Parse the evaluation result
            parsed_result = _parse_evaluation_result(result.final_output)
            return parsed_result
            
    except Exception as e:
        # Return error result
        return {
            "skill_score": 0,
            "cultural_score": 0,
            "overall_score": 0,
            "skill_assessment": f"Error during evaluation: {str(e)}",
            "cultural_assessment": "Could not complete cultural assessment",
            "summary": "Evaluation failed due to technical error",
            "recommendation": "Unable to provide recommendation",
            "error": True
        }

def _parse_evaluation_result(evaluation_text: str) -> dict:
    """Parse the agent's evaluation output to extract structured data."""
    try:
        # Extract scores from Summary Agent's specific format
        skill_score = _extract_summary_score(evaluation_text, "Skill Fit Score")
        cultural_score = _extract_summary_score(evaluation_text, "Cultural Fit Score")
        
        # Calculate overall score
        overall_score = round((skill_score + cultural_score) / 2, 1) if skill_score and cultural_score else 0
        
        # Extract sections from Summary Agent output using bold formatting
        skill_assessment = _extract_bold_section(evaluation_text, "Skill Assessment Summary")
        cultural_assessment = _extract_bold_section(evaluation_text, "Cultural Assessment Summary")
        summary = _extract_section(evaluation_text, ["summary", "overall", "synthesis"])
        recommendation = _extract_bold_section(evaluation_text, "Overall Recommendation")
        
        # Validate that we have assessments from both subagents
        result = _validate_subagent_assessments({
            "skill_score": skill_score,
            "cultural_score": cultural_score,
            "overall_score": overall_score,
            "skill_assessment": skill_assessment,
            "cultural_assessment": cultural_assessment,
            "summary": summary,
            "recommendation": recommendation,
            "raw_output": evaluation_text,
            "error": False
        })
        
        return result
        
    except Exception as e:
        # Fallback parsing
        return {
            "skill_score": 5,  # Default neutral score
            "cultural_score": 5,
            "overall_score": 5,
            "skill_assessment": "Could not parse skill assessment",
            "cultural_assessment": "Could not parse cultural assessment", 
            "summary": evaluation_text[:400] + "..." if len(evaluation_text) > 400 else evaluation_text,
            "recommendation": "Manual review required",
            "raw_output": evaluation_text,
            "error": True
        }

def _extract_score(text: str, keywords: list) -> float:
    """Extract numerical score from text based on keywords"""
    import re
    try:
        # Look for patterns like "8/10", "7 out of 10", "score: 8"
        patterns = [
            r'(\d+(?:\.\d+)?)\s*/\s*10',
            r'(\d+(?:\.\d+)?)\s+out\s+of\s+10',
            r'score[:\s]+(\d+(?:\.\d+)?)',
            r'rating[:\s]+(\d+(?:\.\d+)?)',
        ]
        
        # Search around keywords
        for keyword in keywords:
            for pattern in patterns:
                # Look within 100 characters of keyword
                keyword_pos = text.lower().find(keyword.lower())
                if keyword_pos != -1:
                    context = text[max(0, keyword_pos-50):keyword_pos+100]
                    match = re.search(pattern, context, re.IGNORECASE)
                    if match:
                        score = float(match.group(1))
                        return min(10, max(0, score))  # Clamp between 0-10
        
        return 5.0  # Default neutral score
        
    except:
        return 5.0

def _extract_section(text: str, keywords: list) -> str:
    """Extract text section based on keywords"""
    try:
        lines = text.split('\n')
        
        for keyword in keywords:
            section_lines = []
            capturing = False
            
            for i, line in enumerate(lines):
                line_lower = line.lower().strip()
                
                # Check if this line contains the section header
                if (keyword.lower() in line_lower and 
                    ("assessment" in line_lower or "recommendation" in line_lower or 
                     "synthesis" in line_lower or "summary" in line_lower)):
                    capturing = True
                    continue  # Skip the header line
                
                # If we're capturing and hit another section header, stop
                if capturing and line.startswith('####') and keyword.lower() not in line_lower:
                    break
                
                # If we're capturing, add non-empty lines
                if capturing and line.strip():
                    # Stop at numbered sections or specific markers
                    if line.strip().startswith('#### ') and keyword.lower() not in line_lower:
                        break
                    section_lines.append(line.strip())
            
            if section_lines:
                # Join lines and clean up
                result = ' '.join(section_lines)
                # Remove markdown formatting
                result = result.replace('**', '').replace('*', '')
                return result.strip()
        
        return "Assessment not found"
        
    except Exception as e:
        return f"Could not extract section: {str(e)}"

def _extract_bold_section(text: str, section_name: str) -> str:
    """Extract content from bold-formatted sections like **Skill Assessment Summary**: content"""
    try:
        # Find the section header
        header = f"**{section_name}:**"
        start_pos = text.find(header)
        
        if start_pos == -1:
            return "Assessment not found"
        
        # Find the next ** section or end of text
        content_start = start_pos + len(header)
        next_section = text.find("**", content_start)
        
        if next_section == -1:
            # Extract to end of text
            content = text[content_start:]
        else:
            # Extract until next section
            content = text[content_start:next_section]
        
        # Clean up the content
        content = content.strip()
        # Normalize whitespace but preserve readability
        content = ' '.join(content.split())
        # Remove any remaining asterisks
        content = content.replace('*', '')
        
        return content.strip()
        
    except Exception as e:
        return f"Could not extract bold section: {str(e)}"

def _extract_summary_score(text: str, score_label: str) -> float:
    """Extract scores from Summary Agent format like 'Skill Fit Score: 8.5/10'"""
    try:
        import re
        
        # Look for patterns like "Skill Fit Score: 8.5/10" or "Cultural Fit Score: 9/10"
        pattern = rf'{re.escape(score_label)}:\s*(\d+(?:\.\d+)?)/10'
        match = re.search(pattern, text, re.IGNORECASE)
        
        if match:
            score = float(match.group(1))
            return min(10, max(0, score))  # Clamp between 0-10
        
        # Fallback to original extraction method
        return _extract_score(text, [score_label.lower().split()[0]])
        
    except Exception:
        return 5.0

def _validate_subagent_assessments(result: dict) -> dict:
    """Ensure we have valid assessments from both subagents."""
    
    # Check if skill assessment is missing or too generic
    if (result["skill_assessment"] == "Assessment not found" or 
        len(result["skill_assessment"]) < 50):
        result["skill_assessment"] = f"Skill assessment incomplete. Score: {result['skill_score']}/10. Manual review recommended for technical qualifications."
        result["error"] = True
    
    # Check if cultural assessment is missing or too generic  
    if (result["cultural_assessment"] == "Assessment not found" or 
        len(result["cultural_assessment"]) < 50):
        result["cultural_assessment"] = f"Cultural assessment incomplete. Score: {result['cultural_score']}/10. Manual review recommended for cultural fit."
        result["error"] = True
    
    # Ensure we have a reasonable summary
    if (result["summary"] == "Assessment not found" or 
        len(result["summary"]) < 30):
        result["summary"] = f"Evaluation summary: Skill fit {result['skill_score']}/10, Cultural fit {result['cultural_score']}/10. See individual assessments for details."
    
    return result