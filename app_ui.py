import streamlit as st
import requests
import time

# Configure the web page layout
st.set_page_config(page_title="AI Brand Compliance Dashboard", layout="centered")

st.title("AI Brand Consistency Checker")
st.markdown("Upload any document (.pdf, .docx, .pptx), visual asset (.png, .jpg), or provide a live website URL to run an automated compliance audit against your custom brand rules.")

st.sidebar.header("📋 Brand Guidelines")
# Set a default testing value in the text box so you don't have to retype it every time
rules_input = st.sidebar.text_area(
    "Enter Corporate Rules / Colors:",
    value="The only allowed colors are Cyber Pink #FF007F and Matrix Green #39FF14. We are testing neon styles."
)

# 🌐 INPUT SELECTION LAYER: Allow toggling between files and live websites
input_mode = st.radio("Select Asset Target Type:", ["Uploaded Media File", "Live Website URL"], horizontal=True)

uploaded_file = None
url_input = None

if input_mode == "Uploaded Media File":
    # Create the file uploader drop-zone
    uploaded_file = st.file_uploader("Drag and drop your asset here...", type=["pdf", "docx", "pptx", "png", "jpg", "jpeg"])
else:
    # Create a text box to accept website URLs directly
    url_input = st.text_input("Enter the corporate website URL to audit (e.g., https://example.com/landing):")

# Verify we have an actionable target before enabling the button
has_target = (uploaded_file is not None) if input_mode == "Uploaded Media File" else (url_input and url_input.strip() != "")

if has_target:
    if input_mode == "Uploaded Media File":
        st.info(f"📂 File loaded: {uploaded_file.name}")
    else:
        st.info(f"🌐 Website targeted: {url_input.strip()}")
    
    if st.button("🚀 Run Compliance Audit"):
        with st.spinner("Uploading asset and initializing background processing queue..."):
            try:
                # 1. Prepare data mapping contract for our FastAPI backend
                data = {
                    "request_id": f"ui_{int(time.time())}",
                    "rules_context": rules_input
                }
                
                files = None
                if input_mode == "Uploaded Media File":
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                else:
                    data["target_url"] = url_input.strip()
                
                # 2. Hit the POST endpoint to trigger the job
                response = requests.post("http://127.0.0.1:8000/jobs", files=files, data=data)
                
                if response.status_code == 202:
                    job_id = response.json().get("job_id")
                    st.success(f"✅ Job accepted! ID: {job_id}")
                    
                    # 3. Poll the GET endpoint until the background queue finishes processing
                    status_placeholder = st.empty()
                    while True:
                        status_placeholder.info("⏳ Analyzing content assets and computing brand compliance rubrics...")
                        
                        job_check = requests.get(f"http://127.0.0.1:8000/jobs/{job_id}").json()
                        job_status = job_check.get("status")
                        
                        if job_status == "succeeded":
                            status_placeholder.empty()
                            st.balloons()
                            
                            # Display the final beautiful results payload
                            result_data = job_check.get("result", {})
                            st.subheader("📊 Executive Audit Summary")
                            st.write(result_data.get("summary"))
                            
                            st.subheader("⚠️ Detected Compliance Issues")
                            issues = result_data.get("issues", [])
                            if not issues:
                                st.success("Perfect Compliance! No brand violations found.")
                            for idx, issue in enumerate(issues, 1):
                                with st.expander(f"{idx}. {issue.get('issue_name')}"):
                                    st.error(f"**Offending Element:** {issue.get('offending_text')}")
                                    st.success(f"**Required Correction:** {issue.get('corrected_text')}")
                                    st.caption(f"**Rule Violated:** {issue.get('brand_rule_violated')}")
                            break
                            
                        elif job_status == "failed":
                            status_placeholder.empty()
                            st.error("❌ The analysis engine encountered an execution exception.")
                            st.json(job_check.get("metadata"))
                            break
                            
                        time.sleep(2) # Poll every 2 seconds to keep the event loop lightweight
                else:
                    st.error(f"Backend rejected payload: {response.text}")
            except Exception as e:
                st.error(f"Could not connect to backend gateway: {str(e)}")