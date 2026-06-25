import argparse
import requests
import time
import sys

def run_cli_audit():
    parser = argparse.ArgumentParser(
        description="Production CLI Tool for the AI Brand Consistency Checker Gateway."
    )
    
    # Define our required file and rule inputs matching the FastAPI route contract
    parser.add_argument("--file", required=True, help="Path to the local media asset file to analyze.")
    parser.add_argument("--rules", required=True, help="Plain text string specifying corporate brand guidelines.")
    parser.add_argument("--output", default="compliance_report.md", help="Filename for the saved Markdown report output.")
    
    args = parser.parse_args()

    print(f"🚀 Initializing API Connection to Gateway...")
    print(f"📂 Target Asset: {args.file}")
    
    try:
        # 1. Open the local binary target file to pass through the multipart pipeline
        with open(args.file, "rb") as f:
            files = {"file": (args.file, f, "application/octet-stream")}
            data = {
                "request_id": f"cli_{int(time.time())}",
                "rules_context": args.rules
            }
            
            # 2. Fire the upload request directly to your local background queuing server
            response = requests.post("http://127.0.0.1:8000/jobs", files=files, data=data)
            
        if response.status_code != 202:
            print(f"❌ Server rejected payload initialization: {response.text}")
            sys.exit(1)
            
        job_id = response.json().get("job_id")
        print(f"✅ Secure job allocated to background worker! ID: {job_id}")
        
        # 3. Enter the polling loop until the SQLite execution state flips to terminal
        while True:
            print("⏳ Matrix calculations in progress... checking status...")
            job_check = requests.get(f"http://127.0.0.1:8000/jobs/{job_id}").json()
            status = job_check.get("status")
            
            if status == "succeeded":
                result = job_check.get("result", {})
                summary = result.get("summary", "No summary generated.")
                issues = result.get("issues", [])
                
                # 4. Generate a clean, standards-compliant local Markdown report file
                with open(args.output, "w", encoding="utf-8") as out_file:
                    out_file.write(f"# 🎨 Brand Compliance Audit Report\n\n")
                    out_file.write(f"**Job ID Reference:** `{job_id}`  \n")
                    out_file.write(f"**Target Asset:** `{args.file}`  \n\n")
                    out_file.write(f"## 📊 Executive Summary\n{summary}\n\n")
                    out_file.write(f"## ⚠️ Detected Compliance Issues ({len(issues)})\n\n")
                    
                    if not issues:
                        out_file.write("✨ Perfect Compliance! No violations found matching your rules matrix.\n")
                    else:
                        for idx, issue in enumerate(issues, 1):
                            out_file.write(f"### {idx}. {issue.get('issue_name')}\n")
                            out_file.write(f"* **Offending Text/Element:** `{issue.get('offending_text')}`\n")
                            out_file.write(f"* **Required Actionable Correction:** {issue.get('corrected_text')}\n")
                            out_file.write(f"* **Brand Rule Violated:** *\"{issue.get('brand_rule_violated')}\"*\n\n")
                
                print(f"\n🎉 Audit complete! Local compliance report compiled cleanly to: **{args.output}**")
                break
                
            elif status == "failed":
                print("\n❌ The background orchestration layer encountered an execution exception.")
                print(job_check.get("metadata"))
                sys.exit(1)
                
            time.sleep(2) # Keep polling thread safe and light
            
    except FileNotFoundError:
        print(f"❌ Error: The local file target path '{args.file}' does not exist.")
    except requests.exceptions.ConnectionError:
        print("❌ Error: Gateway unavailable. Ensure your Uvicorn server loop is running on port 8000.")

if __name__ == "__main__":
    run_cli_audit()