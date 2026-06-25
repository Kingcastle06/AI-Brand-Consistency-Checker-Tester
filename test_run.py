import os
from dotenv import load_dotenv

# 1. Fire up the vault loader to inject your keys into memory securely from .env
load_dotenv()

# 2. Import your production orchestration engine
from ai_brand_consistency_checker.orchestrator import run_brand_check

# 3. Define the 'bad' marketing copy breaking our specific rules
sample_copy = (
    "Our new hyperloop braking mechanism is super sick and totally works via liquid calipers "
    "or whatever. It slows down the pod pretty fast."
)

# 4. Set the strict engineering guidelines we want Gemini to enforce
company_rules = (
    "1. Always maintain a professional, academic engineering tone.\n"
    "2. Technical accuracy constraint: The braking system is strictly PNEUMATIC (air-based), never liquid-based."
)

print("🚀 Launching live end-to-end telemetry check securely with Google Gemini...")

try:
    # 5. Trigger the orchestrator pipeline
    output_envelope = run_brand_check(
        text_to_check=sample_copy, rules_context=company_rules
    )

    print("\n🟢 SUCCESS! Production CheckerOutput Generated Perfectly:")
    print("=" * 60)
    print(f"Job ID:   {output_envelope.job_id}")
    print(f"Status:   {output_envelope.status.value.upper()}")
    print(f"Metadata: {output_envelope.metadata}")
    print("=" * 60)

    # 6. Extract and print the domain results from the validated Pydantic dictionary
    analysis_result = output_envelope.result
    print(f"\nSummary: {analysis_result.get('summary')}")
    print("-" * 60)

    for i, issue in enumerate(analysis_result.get("issues", []), 1):
        print(f"\n[Brand Violation #{i}]")
        print(f"  Headline:       {issue.get('headline')}")
        print(f"  Offending Text: '{issue.get('offending_text')}'")
        print(f"  Corrected Text: '{issue.get('corrected_text')}'")
        print(f"  Rule Violated:  {issue.get('brand_rule_violated')}")

except Exception as e:
    print(f"\n🔴 CRITICAL SYSTEM FAILURE: {e}")