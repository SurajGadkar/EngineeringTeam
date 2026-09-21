"""Planner Agent — converts user prompt into production MERN plan with AI integration."""
from pathlib import Path
from agents.base_agent import llm_chat, write_artifact, read_artifact

WORK = Path("/home/ubuntu/engineering-team/workspace")

def run(prompt: str) -> Path:
    WORK.mkdir(exist_ok=True)
    planning_prompt = f"""You are the Planning Engineer of an Engineering Team building production-grade MERN apps.
Given this user prompt: \"{prompt}\"
Produce a structured PLAN in markdown with these sections:
1. Product Vision & Features
2. MERN Architecture (MongoDB schema, Express routes, React UI, AI integration with openRouter/free model)
3. Tech Stack decisions (include any additional open-source packages needed)
4. Milestones (Plan → Dev → Test → QA → Deploy)
5. Test Strategy (unit, integration, e2e, AI response validation)
6. QA Signoff Criteria (all tests pass, security reviewed, responsive, AI integration responsive)
Keep concise (under 400 lines, structured with headers)."""
    plan_md = llm_chat(planning_prompt, model="openai/gpt-3.5-turbo", max_tokens=3000, temperature=0.2)
    out = WORK / "plan.md"
    # If LLM unavailable, inject a robust default plan
    if "[LLM" in plan_md or len(plan_md) < 200:
        plan_md = generate_default_plan(prompt)
    write_artifact(out, plan_md)
    print(f"[PLANNER] Wrote plan to {out} ({len(plan_md)} chars)")
    return out

def generate_default_plan(prompt: str) -> str:
    return f"""# Engineering Plan — MERN + AI

## Prompt
{prompt}

## Vision
AI-powered web application with user auth, CRUD, and an openRouter/free AI chatbot.

## Architecture
- MongoDB via Mongoose (users, tasks, messages collections)
- Express REST API (auth, tasks, ai/chat endpoints)
- React (Vite) SPA with AI chat widget
- OpenRouter/free: `openai/gpt-3.5-turbo` via server proxy (no key exposure)

## Additional Tech
- `express`, `mongoose`, `cors`, `bcryptjs`, `jsonwebtoken`
- Client: `react`, `axios`, `react-router-dom`
- Tests: `vitest` (client), `jest`/`supertest` (server)
- Docker for deployment

## Milestones (max 5 iterations)
1. Plan / Setup
2. Backend + DB + AI proxy
3. Frontend + AI widget
4. Tests + QA review
5. Deploy / Signoff

## QA Criteria
- All backend + frontend tests pass (>=95%)
- AI endpoint responds within 5s
- Responsive design
- Security (no exposed keys, hashed passwords, CORS restricted)
"""
