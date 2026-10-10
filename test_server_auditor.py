
from src.server_auditor import audit_server_properties

sample_config = """
online-mode=false
white-list=false
enable-rcon=true
"""

findings = audit_server_properties(sample_config)

print("GameGuard Server Security Check")
print("-" * 35)

for finding in findings:
    print(f"\nSeverity: {finding['severity']}")
    print(f"Setting: {finding['setting']}")
    print(f"Finding: {finding['finding']}")
    print(f"Recommendation: {finding['recommendation']}")
