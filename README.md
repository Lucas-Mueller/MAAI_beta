# 🎯 CV Assessment System

An AI-powered application for evaluating job candidates using multi-agent assessment. Upload job descriptions and CVs to get detailed evaluations across skill fit, cultural fit, and overall compatibility.

## Features

- **PDF Upload**: Upload job descriptions and candidate CVs as PDF files
- **Multi-Agent Evaluation**: Uses specialized AI agents for comprehensive assessment
- **Detailed Scoring**: Get numerical scores and detailed text assessments
- **Clean Interface**: Simple, intuitive web interface
- **Job History**: Track multiple evaluation sessions

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up Environment**
   ```bash
   # Create .env file with your OpenAI API key
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   ```

3. **Start the Application**
   ```bash
   python run.py
   ```

4. **Open Browser**
   Navigate to `http://localhost:8000`

## How It Works

### 1. Upload Job Description
- Upload a PDF containing the job requirements
- System extracts and processes the text

### 2. Upload Candidate CVs
- Upload multiple CV PDFs for evaluation
- Each CV is processed individually

### 3. AI Evaluation
- **Skill Fit Agent**: Evaluates technical qualifications and experience
- **Cultural Fit Agent**: Assesses cultural alignment and soft skills
- **Main Agent**: Synthesizes results and provides recommendations

### 4. Review Results
- View ranked candidates with detailed scores
- Expand each candidate for comprehensive assessment
- Export or save results for further review

## File Structure

```
MAAI_beta/
├── app.py                 # FastAPI application
├── run.py                 # Startup script
├── agent_system.py        # Original multi-agent system
├── agents_configs.py      # Agent prompts and configurations
├── backend/
│   ├── cv_evaluator.py    # CV evaluation logic
│   ├── pdf_processor.py   # PDF text extraction
│   └── database.py        # SQLite database operations
├── frontend/
│   ├── index.html         # Main web interface
│   └── static/
│       ├── style.css      # Styling
│       └── script.js      # Frontend logic
├── mcp_servers/           # MCP server implementations
└── knowledge_base/        # Documentation and examples
```

## Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)
-  `BRAVE_API_KEY`: Your BRAVE API key (required for MCP tool use of BRAVE, free option available)

### Agent Settings
Edit `agents_configs.py` to customize:
- Agent prompts and instructions
- Evaluation criteria
- Scoring methodology

## API Endpoints

- `POST /upload/job-description` - Upload job description PDF
- `POST /upload/cvs/{job_id}` - Upload CV PDFs for a job
- `POST /evaluate/{job_id}` - Start evaluation process
- `GET /results/{job_id}` - Get evaluation results
- `GET /jobs` - List all jobs

## Database

Uses SQLite for simplicity and portability:
- **job_descriptions**: Job posting details
- **cvs**: Candidate CV information
- **evaluations**: Assessment results and scores

## Development

### Adding New Evaluation Criteria
1. Update agent prompts in `agents_configs.py`
2. Modify result parsing in `backend/cv_evaluator.py`
3. Update database schema if needed

### Customizing UI
- Edit `frontend/static/style.css` for styling
- Modify `frontend/static/script.js` for behavior
- Update `frontend/index.html` for layout

## Troubleshooting

### Common Issues
1. **Import Errors**: Ensure all dependencies are installed
2. **API Key Issues**: Check `.env` file configuration
3. **PDF Processing**: Verify PDF files are not password-protected
4. **Database Errors**: Delete `cv_assessment.db` to reset

### Logs
Check console output for detailed error messages and debugging information.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

