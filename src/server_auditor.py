
def audit_server_properties(config_text):
    """
    Basic checks for Minecraft Java server.properties.
    This is a rule-based prototype, not a complete security audit.
    """
    settings = {}

    for line in config_text.splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        settings[key.strip()] = value.strip()

    findings = []

    if settings.get("online-mode", "true").lower() == "false":
        findings.append({
            "severity": "HIGH",
            "setting": "online-mode",
            "finding": "Online authentication is disabled.",
            "recommendation": (
                "For a normal public server, enable online-mode=true. "
                "Only use alternative authentication setups with "
                "appropriate trusted protections."
            ),
        })

    if settings.get("white-list", "false").lower() != "true":
        findings.append({
            "severity": "MEDIUM",
            "setting": "white-list",
            "finding": "The player whitelist is not enabled.",
            "recommendation": (
                "If the server is intended for a private group, "
                "consider enabling white-list=true."
            ),
        })

    if settings.get("enable-rcon", "false").lower() == "true":
        findings.append({
            "severity": "HIGH",
            "setting": "enable-rcon",
            "finding": "Remote Console (RCON) is enabled.",
            "recommendation": (
                "Disable RCON if it is not needed. If required, "
                "protect it with a strong secret and network restrictions."
            ),
        })

    if not findings:
        findings.append({
            "severity": "INFO",
            "setting": "general",
            "finding": "No issues covered by these basic checks were found.",
            "recommendation": (
                "This does not prove the server is secure. Review "
                "network exposure, permissions, software updates, "
                "and other settings separately."
            ),
        })

    return findings
