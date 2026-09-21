#!/bin/bash
# Trigger the Agentic Pipeline workflow
# Usage: ./scripts/trigger-pipeline.sh <feature_name> [description] [branch_name]
#
# Example: ./scripts/trigger-pipeline.sh "user-auth" "JWT-based auth system" "feat/user-auth-2026"

FEATURE_NAME="${1:?Usage: ./trigger-pipeline.sh <feature_name> [description] [branch_name]}"
DESCRIPTION="${2:-}"
BRANCH="${3:-}"

echo "🔧 Triggering Agentic Pipeline for: $FEATURE_NAME"
echo "   Description: ${DESCRIPTION:-(none)}"
echo "   Branch: ${BRANCH:-(auto-generated)}"
echo ""

gh workflow run agentic-pipeline.yml \
  -f feature_name="$FEATURE_NAME" \
  -f description="$DESCRIPTION" \
  -f branch="$BRANCH"

echo ""
echo "✅ Pipeline triggered! Check the Actions tab for status:"
echo "   https://github.com/SurajGadkar/EngineeringTeam/actions"
echo ""
echo "The agent will:"
echo "  1. Build the feature on a feature branch"
echo "  2. Run tests"
echo "  3. Open a PR against main"
echo "  4. Wait for YOUR approval before merge"
