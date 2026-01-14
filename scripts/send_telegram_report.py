import os
import requests
import xml.etree.ElementTree as ET

BOT_TOKEN = os.environ["TGBOT"]
CHAT_ID = os.environ["CHATID"]
RUN_ID = os.environ["RUN_ID"]
REPO = os.environ.get("GITHUB_REPOSITORY", "unknown")

REPORT_PATH = "reports/newman-report.xml"

# --- Parse JUnit ---
tree = ET.parse(REPORT_PATH)
root = tree.getroot()

tests = int(root.attrib.get("tests", 0))
failures = int(root.attrib.get("failures", 0))
errors = int(root.attrib.get("errors", 0))

failed = failures + errors
passed = tests - failed

status = "success ✅" if failed == 0 else "failed ❌"

message = f"""
🚀 Прогон коллекции Flipper завершен

Repo: {REPO}
Branch: main
Status: {status}

Tests summary:
• ✅ Passed: {passed}
• ❌ Failed: {failed}
• 🧪 Total: {tests}

Links:
• 🔗 HTML Report:
https://nikitamiloserdov.github.io/fl-test/runs/{RUN_ID}/
""".strip()

response = requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    json={
        "chat_id": CHAT_ID,
        "text": message
    },
    timeout=10
)

response.raise_for_status()

