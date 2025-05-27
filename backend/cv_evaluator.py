"""
CV evaluation system using multi-agent approach.
Integrates with the existing agent system for candidate assessment.
"""
from agents import Agent, Runner
import asyncio
import json
from typing import Dict, Any
import re
import sys
import os

# Add parent directory to path to import agents_configs
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents_configs import (
    SKILL_FIT_AGENT_DESCRIPTION,
    CULTURAL_FIT_AGENT_DESCRIPTION, 
    MAIN_AGENT_DESCRIPTION
)

class CVEvaluator:
    """Handles CV evaluation using multi-agent system"""
    
    def __init__(self):
        """Initialize the multi-agent system"""
        self.model = "gpt-4.1"
        self._setup_agents()
    
    def _setup_agents(self):
        """Set up the agent system with proper handoffs"""
        # Define agents
        self.main_agent = Agent(
            model=self.model,
            name="Main Agent",
            instructions=MAIN_AGENT_DESCRIPTION,
        )

        self.cultural_fit_agent = Agent(
            model=self.model,
            name="Cultural Fit Agent",
            instructions=CULTURAL_FIT_AGENT_DESCRIPTION,
        )

        self.skill_fit_agent = Agent(
            model=self.model,
            name="Skill Fit Agent",
            instructions=SKILL_FIT_AGENT_DESCRIPTION,
        )

        # Set up handoff chain
        self.main_agent.handoffs = [self.skill_fit_agent, self.cultural_fit_agent]
        self.skill_fit_agent.handoffs = [self.main_agent]
        self.cultural_fit_agent.handoffs = [self.main_agent]
    
    async def evaluate_cv(self, job_description: str, cv_text: str) -> Dict[str, Any]:
        """
        Evaluate a CV against a job description using multi-agent system.
        
        Args:
            job_description: Text content of the job description
            cv_text: Text content of the CV
            
        Returns:
            Dictionary containing evaluation results with scores and assessments
        """
        try:
            # Prepare input for the agent system
            evaluation_input = f"""Please evaluate this candidate:

CV:
{cv_text}

Job Description:
{job_description}"""

            # Run the evaluation
            result = Runner.run_streamed(
                self.main_agent,
                input=evaluation_input,
                max_turns=10
            )
            
            # Wait for completion and get final output
            final_output = ""
            async for event in result.stream_events():
                pass  # Process events if needed for monitoring
            
            final_output = result.final_output
            
            # Parse the evaluation result
            parsed_result = self._parse_evaluation_result(final_output)
            
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
    
    def _parse_evaluation_result(self, evaluation_text: str) -> Dict[str, Any]:
        """
        Parse the agent's evaluation output to extract structured data.
        
        Args:
            evaluation_text: Raw output from the agent system
            
        Returns:
            Structured evaluation result
        """
        try:
            # Extract scores using regex patterns
            skill_score = self._extract_score(evaluation_text, ["skill", "technical"])
            cultural_score = self._extract_score(evaluation_text, ["cultural", "culture", "fit"])
            
            # Calculate overall score
            overall_score = round((skill_score + cultural_score) / 2, 1) if skill_score and cultural_score else 0
            
            # Extract text sections
            skill_assessment = self._extract_section(evaluation_text, ["skill", "technical"])
            cultural_assessment = self._extract_section(evaluation_text, ["cultural", "culture"])
            summary = self._extract_section(evaluation_text, ["summary", "overall", "synthesis"])
            recommendation = self._extract_section(evaluation_text, ["recommendation", "recommend"])
            
            return {
                "skill_score": skill_score,
                "cultural_score": cultural_score,
                "overall_score": overall_score,
                "skill_assessment": skill_assessment,
                "cultural_assessment": cultural_assessment,
                "summary": summary,
                "recommendation": recommendation,
                "raw_output": evaluation_text,
                "error": False
            }
            
        except Exception as e:
            # Fallback parsing
            return {
                "skill_score": 5,  # Default neutral score
                "cultural_score": 5,
                "overall_score": 5,
                "skill_assessment": "Could not parse skill assessment",
                "cultural_assessment": "Could not parse cultural assessment", 
                "summary": evaluation_text[:500] + "..." if len(evaluation_text) > 500 else evaluation_text,
                "recommendation": "Manual review required",
                "raw_output": evaluation_text,
                "error": True
            }
    
    def _extract_score(self, text: str, keywords: list) -> float:
        """Extract numerical score from text based on keywords"""
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
    
    def _extract_section(self, text: str, keywords: list) -> str:
        """Extract text section based on keywords"""
        try:
            text_lower = text.lower()
            
            for keyword in keywords:
                keyword_pos = text_lower.find(keyword.lower())
                if keyword_pos != -1:
                    # Find the section starting from keyword
                    start = keyword_pos
                    # Look for next section or end
                    next_section = min([
                        pos for pos in [
                            text_lower.find('\n\n', start + 50),
                            text_lower.find('**', start + 10),
                            text_lower.find('##', start + 10),
                            len(text)
                        ] if pos != -1
                    ])
                    
                    section = text[start:next_section].strip()
                    if len(section) > 20:  # Only return substantial sections
                        return section
            
            return "Assessment not found"
            
        except:
            return "Could not extract section"