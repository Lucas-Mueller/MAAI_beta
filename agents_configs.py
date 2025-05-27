SKILL_FIT_AGENT_DESCRIPTION = '''You are a Skill Fit Evaluator. You will receive a CV and job description.

Your task is to evaluate technical and professional qualifications. Assess:
- Relevant technical skills and tools
- Work experience alignment with job responsibilities
- Education and certifications
- Domain expertise and accomplishments

Important: Use the brave search tool via MCP to research on the reputation of the candidates university

Rate the candidate's skill fit out of 10 and provide your assessment.

IMPORTANT: After providing your assessment, ALWAYS hand off to the Cultural Fit Agent using the transfer tool.
'''

CULTURAL_FIT_AGENT_DESCRIPTION = '''You are a Cultural Fit Evaluator. You will receive a CV, job description, AND the skill fit evaluation from the previous agent.

Your task is to evaluate cultural fit objectively and fairly. Assess:
- Communication style and collaboration approach
- Professional values and work environment preferences  
- Alignment with company culture and mission
- Team dynamics and cultural compatibility

Rate the candidate's cultural fit out of 10 and provide your assessment based purely on merit and job-relevant criteria.

IMPORTANT: After providing your assessment, ALWAYS hand off to the Main Agent using the transfer tool for final synthesis.
'''

MAIN_AGENT_DESCRIPTION = '''You are the Main Coordinator for candidate evaluation. 

When you receive the initial request with CV and job description:
give it to the respective agents at your disposal to get their assesment

When you receive handoffs with BOTH skill and cultural evaluations:
- Create a final synthesis that includes:
  - Summary of skill fit assessment (with score)
  - Summary of cultural fit assessment (with score)
  - Overall strengths and potential concerns
  - Any alignment or disconnect between skill and cultural fit
  - A brief recommendation on whether the applicant should proceed

Your final output should be professional and readable, similar to a recruiter's internal summary.

IMPORTANT: Only hand off to Skill Fit Agent at the very beginning. When you receive the final handoff from Cultural Fit Agent, provide the synthesis and DO NOT hand off again.
'''

JOB_EXAMPLE = """
Position: Digital Marketing Manager  
Location: Berlin, Germany (Hybrid)

About Us:  
At **Harmonia Collective**, we're a purpose-driven lifestyle brand focused on wellness, sustainability, and creative expression. Our team is small, agile, and deeply collaborative. We believe in open communication, shared learning, and building a culture where everyone feels ownership and belonging.

What We're Looking For:  
We're searching for a **Digital Marketing Manager** who is both strategically minded and creatively driven. You should be someone who thrives in cross-functional teams, communicates clearly, and understands the power of authentic branding. You care about sustainability, value diversity, and are comfortable taking initiative while remaining aligned with team goals.

Responsibilities:
- Develop and execute digital marketing campaigns across email, social media, and web
- Manage and mentor a small team of creatives and marketers
- Collaborate with product, design, and customer experience teams to ensure brand consistency
- Analyze campaign performance and optimize based on data
- Support content development with strong storytelling and attention to tone

Requirements:
- 5+ years experience in digital marketing, preferably in a startup or fast-paced environment
- Experience managing or mentoring team members
- Strong skills in SEO, SEM, and content marketing
- Proficiency with marketing tools (e.g., HubSpot, Google Analytics)
- Excellent communication and project management skills
- Passion for sustainability, wellness, or ethical brands is a plus

Company Culture:
- Weekly team check-ins and async-friendly workflows
- Emphasis on mental well-being and work-life balance
- Team events, both in-person and remote
- Encouragement of personal growth and continuous learning

Language: English is our working language; German is a plus but not required.
"""

CV_EXAMPLE = """
Name: Anna Keller
Location: Berlin, Germany

Summary:
A collaborative and creative marketing professional with over 6 years of experience in digital strategy, content creation, and brand development. Passionate about building authentic connections between brands and audiences. Known for thriving in fast-paced, cross-functional teams and bringing a people-first mindset to every project.

Experience:
Marketing Manager – BrightWorks GmbH, Berlin (March 2021 – Present)
- Developed and led integrated campaigns across social, web, and email, increasing lead generation by 35% YoY
- Managed a team of 3 and collaborated closely with design and product teams
- Spearheaded internal branding initiatives that improved employee engagement scores by 15%

Content Strategist – Wave Studio, Remote (June 2018 – February 2021)
- Created content roadmaps and editorial calendars for 5+ B2B clients
- Led client workshops to align messaging strategies with customer personas
- Contributed to a culture of open feedback and continuous learning

Education: B.A. in Communication Science – University of TU Munich, 2013–2017

Skills: Digital Marketing (SEO, SEM, Email), Content Strategy & Writing, Project Management Tools (Asana, Trello), Adobe Creative Suite

Languages: German (Native), English (Fluent), Spanish (Basic)

Interests: Volunteering in local mentorship programs, Sustainability and ethical branding, Remote work advocacy
"""