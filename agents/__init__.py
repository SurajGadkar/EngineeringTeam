"""Engineering Team — Multi-Agent MERN Builder Framework.
Agents: Planner → Developer → Tester → QA → DevOps (loop with feedback)."""
VERSION = "1.0.0"
MAX_ITERATIONS = 5
OPENROUTER_FREE_MODEL = "openai/gpt-3.5-turbo"  # openRouter/free tier
APP_PROMPT_DEFAULT = ("Build an AI-powered task manager with MERN stack. "
    "Features: user auth, CRUD tasks, AI chat assistant using openRouter/free, "
    "responsive UI, REST API with tests, Docker-ready. Produce production-grade code.")
