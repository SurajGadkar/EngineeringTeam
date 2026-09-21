"""QA Agent — reviews tests, code quality, security, AI integration; produces signoff."""
import json
from pathlib import Path
from agents.base_agent import llm_chat, read_artifact

WORK = Path("/home/ubuntu/engineering-team/workspace/app")

def run(plan_path: Path, test_path: Path, iteration: int) -> Path:
    test_text = read_artifact(test_path) if test_path.exists() else "{}"
    code_dir = WORK / "developer_output.md"
    prompt = f"""You are a QA Engineer reviewing an Engineering Team output (iteration {iteration}).
Plan: {read_artifact(plan_path)[:2000]}
Test results: {test_text[:1000]}
Check:
- Are all required features present (auth, AI chat, CRUD)?
- Are tests passing (status passed)?
- Security: no hardcoded secrets? CORS set? JWT used properly?
- AI integration references openRouter/free model?
- Is code production-grade?
Return ONLY JSON: {{"signoff": true/false, "notes": "...", "required_fixes": ["..."], "production_ready": true/false}}."""
    review = llm_chat(prompt, model="openai/gpt-3.5-turbo", max_tokens=1500, temperature=0.1)
    # If LLM unavailable, apply structured heuristics
    if "[LLM" in review or "{" not in review:
        review = generate_heuristic_qa(test_text, code_dir.exists())
    else:
        # Try to clean to JSON
        try:
            # Extract first JSON block
            start = review.index("{")
            end = review.rindex("}") + 1
            json.loads(review[start:end])
        except Exception:
            review = generate_heuristic_qa(test_text, code_dir.exists())
    out = WORK / "qa_report.json"
    out.write_text(review, encoding="utf-8")
    print(f"[QA] Iteration {iteration} — signoff={json.loads(read_artifact(out)).get('signoff')}")
    return out

def generate_heuristic_qa(test_json_str: str, code_exists: bool) -> str:
    try:
        data = json.loads(test_json_str)
    except Exception:
        data = {}
    signoff = data.get("status", "unknown") == "passed" and code_exists
    return json.dumps({
        "signoff": signoff,
        "notes": f"Heuristic QA: code present={code_exists}, tests={data.get('tests', [])}. {'PASS — production ready' if signoff else 'FAIL — fix before deploy'}",
        "required_fixes": ["Add OPENROUTER_API_KEY to .env", "Run npm install + tests"] if not signoff else [],
        "production_ready": signoff,
        "iteration": data.get("iteration", 1)
    }, indent=2)
