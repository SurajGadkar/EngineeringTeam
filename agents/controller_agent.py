"""Controller Agent — orchestrates Planning → Dev → Test → QA → Deploy loop (max 5 iterations)."""
import sys, time
sys.path.insert(0, "/home/ubuntu/engineering-team/agents")
from pathlib import Path
import planner_agent, developer_agent, tester_agent, qa_agent, devops_agent
from agents.base_agent import read_artifact, write_artifact
import json

WORK = Path("/home/ubuntu/engineering-team/workspace")

def run(prompt: str = ""):
    from agents import APP_PROMPT_DEFAULT
    user_prompt = prompt or APP_PROMPT_DEFAULT
    WORK.mkdir(exist_ok=True)
    status = {"iterations": 0, "max": 5, "final_status": "in-progress", "history": []}

    # Step 1: Plan
    plan_path = planner_agent.run(user_prompt)

    # Step 2-5: Loop
    for i in range(1, 6):
        status["iterations"] = i
        print(f"\n=== ENGINEERING TEAM — ITERATION {i} ===")

        # Developer
        prev_qa = WORK / "qa_report.json"
        feedback = ""
        if prev_qa.exists():
            data = json.loads(read_artifact(prev_qa))
            fixes = data.get("required_fixes", [])
            notes = data.get("notes", "")
            feedback = f"Previous QA: {notes}. Fixes needed: {fixes}."
        dev_path = developer_agent.run(plan_path, iteration=i, feedback=feedback)

        # Tester
        test_path = tester_agent.run(plan_path, iteration=i)

        # QA
        qa_path = qa_agent.run(plan_path, test_path, iteration=i)
        qa_data = json.loads(read_artifact(qa_path))
        signoff = qa_data.get("signoff", False)
        production_ready = qa_data.get("production_ready", False)

        # DevOps (always update deploy artifacts)
        devops_agent.run(i)

        # Record
        status["history"].append({
            "iteration": i,
            "dev_path": str(dev_path),
            "test_path": str(test_path),
            "qa_path": str(qa_path),
            "signoff": signoff,
            "production_ready": production_ready,
            "feedback_next": feedback,
        })

        # Break if production-ready and QA signoff
        if signoff and production_ready:
            status["final_status"] = "production-ready"
            print(f"=== PRODUCTION READY AT ITERATION {i} ===")
            break
        else:
            status["final_status"] = f"needs-iteration-{i+1}"
            print(f"=== NOT READY — feedback for next iteration ===")
            for f in qa_data.get("required_fixes", []):
                print(f"  - FIX: {f}")

    # Final status
    out = WORK / "final_status.json"
    out.write_text(json.dumps(status, indent=2))
    print(f"\n=== ENGINEERING TEAM COMPLETE ===")
    print(f"Status: {status['final_status']}")
    print(f"History: {len(status['history'])} iterations (max 5)")
    print(f"Artifacts in: {WORK}")
    return out

if __name__ == "__main__":
    prompt_arg = sys.argv[1] if len(sys.argv) > 1 else ""
    run(prompt_arg)
