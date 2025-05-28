# CV Evaluation System Design Documentation

## Overview
This document explains the design decisions, challenges, and solutions implemented in the CV evaluation system. It serves as a reference for future development and maintenance.

## System Architecture

### Core Components
```
FastAPI App (app.py)
├── PDF Processing (backend/pdf_processor.py)
├── Database Operations (backend/database.py)
└── CV Evaluation (cv_agents/)
    ├── Agent System (agent_system.py)
    └── Agent Configurations (agents_configs.py)
```

### Agent-Based Evaluation Flow
1. **Main Agent** receives job description + CV
2. **Skill Fit Agent** evaluates technical qualifications
3. **Cultural Fit Agent** evaluates cultural alignment  
4. **Summary Agent** creates concise summaries of both evaluations
5. **Main Agent** receives summaries and creates final synthesis

## Key Design Decisions

### 1. Multi-Agent Architecture
**Decision**: Use 4 specialized agents instead of a single evaluation agent.

**Rationale**:
- **Separation of concerns**: Each agent focuses on specific evaluation criteria
- **Better accuracy**: Specialized prompts for technical vs cultural assessment
- **Length control**: Dedicated Summary Agent creates user-friendly summaries
- **Modularity**: Easy to modify individual agent behavior without affecting others
- **Clean handoff flow**: Linear agent progression ensures all evaluations are completed

**Implementation**: 
- Skill Fit Agent: Technical skills, experience, qualifications
- Cultural Fit Agent: Values, communication style, team fit
- Summary Agent: Concise summaries of both evaluations for frontend display
- Main Agent: Orchestration and final synthesis

### 2. Dynamic Handoff System
**Challenge**: The main agent dynamically chooses which subagents to call, potentially skipping assessments.

**Solution Implemented**:
- **Mandatory workflow instructions** in main agent prompt
- **Validation functions** to detect missing assessments
- **Fallback messaging** when subagent assessments are incomplete
- **Error flagging** when critical assessments are missing

**Code Location**: `_validate_subagent_assessments()` in `agent_system.py`

### 3. Text Length Management
**Challenge**: Agent outputs can be excessively long, creating poor UX.

**Solution Implemented**:
- **Summary Agent**: Dedicated agent creates 2-3 sentence summaries
- **Agent-driven length control**: Length managed by prompt engineering, not post-processing
- **Natural language**: Summaries are coherent and contextual, not arbitrarily truncated
- **Preserved detail**: Full evaluations stored but summaries displayed to users

**Code Location**: `SUMMARY_AGENT_DESCRIPTION` in `agents_configs.py`

### 4. Robust Parsing System
**Challenge**: Extract structured data from unstructured agent output.

**Approach**:
- **Section-based parsing** using markdown headers (#### Skill Fit Assessment)
- **Regex score extraction** for numerical ratings
- **Fallback mechanisms** when parsing fails
- **Content validation** to ensure meaningful assessments

## Critical Implementation Details

### Agent Prompt Engineering
- **Explicit workflows**: MANDATORY steps in main agent instructions
- **Consistent output format**: Agents trained to use specific section headers
- **Score requirements**: Always include numerical ratings (X/10 format)
- **Handoff instructions**: Clear guidance on when to transfer to next agent

### Error Handling Strategy
1. **Graceful degradation**: System continues working even with partial failures
2. **Fallback content**: Meaningful messages when parsing fails
3. **Error flagging**: Results marked with error status for manual review
4. **Raw output preservation**: Always store complete agent response for debugging

### Performance Optimizations
- **Minimal imports**: Removed unused dependencies
- **Efficient parsing**: Single-pass text processing where possible
- **Lazy loading**: MCP servers only loaded when needed
- **Clean architecture**: Separation of concerns reduces complexity

## Configuration Management

### Model Selection
- **Current**: GPT-4.1 for balance of capability and cost
- **Alternatives**: Can switch to GPT-4.1-mini/nano for cost optimization
- **Centralized**: Single model setting for all agents

### MCP Servers
- **Brave Search**: For university reputation research (Skill Fit Agent)
- **Arxiv/Zotero**: Available but not actively used in current workflow
- **Modular**: Easy to add/remove additional tools

## Testing Strategy

### Validation Checkpoints
1. **Import validation**: Ensure clean module imports
2. **Function isolation**: Test individual parsing functions
3. **End-to-end flow**: Complete evaluation workflow
4. **Error scenarios**: Missing assessments, parsing failures

### Quality Assurance
- **Length validation**: Ensure truncation works correctly
- **Content validation**: Verify meaningful assessments are generated
- **Score validation**: Confirm numerical ratings are extracted
- **Format validation**: Check output structure consistency

## Future Considerations

### Scalability
- **Database**: SQLite suitable for development, consider PostgreSQL for production
- **Async processing**: Current implementation supports concurrent evaluations
- **Caching**: Consider caching agent responses for similar CVs

### Extensibility
- **Additional agents**: Easy to add specialized evaluators (e.g., Leadership Assessment)
- **Custom criteria**: Modify agent prompts for different job types
- **Integration**: MCP framework allows easy addition of external tools

### Monitoring
- **Evaluation metrics**: Track assessment quality and consistency
- **Performance monitoring**: Agent response times and success rates
- **Error tracking**: Monitor parsing failures and validation issues

## Known Limitations

1. **Agent reliability**: Dependent on LLM following instructions consistently
2. **Parsing brittleness**: Text-based parsing can fail with format changes
3. **Language dependency**: Currently optimized for English content
4. **Subjective scoring**: Cultural fit scores inherently subjective

## Code Maintenance Guidelines

### Adding New Features
1. **Test in isolation**: Validate new parsing functions independently
2. **Maintain backwards compatibility**: Preserve existing API contracts
3. **Update validation**: Extend `_validate_subagent_assessments()` for new fields
4. **Document changes**: Update this file with new design decisions

### Debugging Issues
1. **Check raw output**: Review `raw_output` field in evaluation results
2. **Validate parsing**: Test individual `_extract_section()` calls
3. **Review agent logs**: Monitor handoff patterns in agent system
4. **Verify prompts**: Ensure agent instructions are being followed

---

*Last updated: January 2025*
*System version: 1.0*