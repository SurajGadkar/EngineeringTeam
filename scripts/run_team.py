#!/usr/bin/env python3
"""Run the Engineering Team from CLI: python scripts/run_team.py [prompt]"""
import sys, os
sys.path.insert(0, "/home/ubuntu/engineering-team")
os.chdir("/home/ubuntu/engineering-team")
from agents.controller_agent import run
if __name__ == "__main__":
    prompt = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    if not prompt:
        prompt = "AI-powered task manager with MERN stack, openRouter/free AI chat, user auth, responsive UI, Docker deploy"
    run(prompt)
