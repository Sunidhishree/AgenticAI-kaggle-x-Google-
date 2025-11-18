Distributed Intrusion Detection & Response System (D-IDRS)

This project implements a Sequential Multi-Agent Intrusion Detection & Response System built using the Google ADK (Agent Development Kit). The system simulates a real-world SOC (Security Operations Center) pipeline where AI agents collaboratively analyze raw alerts, take mitigation actions, generate visual summaries, and produce a final incident report. All operations flow through a shared session state to maintain context across the lifecycle.

Overview

D-IDRS follows a strict four-step security workflow:

Correlation of incoming alerts using historical memory

Mitigation using an IP blocking tool

Infographic generation summarizing the incident

Final report generation

Each agent is specialized and connected through the session state, ensuring continuity and accuracy.

Architecture Summary

Raw Alerts
↓
CorrelationAgent → produces incident_report
↓
MitigationAgent → uses BlockIPTool and produces mitigation_status
↓
InfographicAgent → generates image and produces security_image_result
↓
ReportingAgent → reads everything and generates final report
↓
Final Output to User or Dashboard

Agent Roles and Responsibilities

RootAgent (Sequential Orchestrator)
Type: SequentialAgent
Role: Controls and executes the entire workflow. Ensures each step flows into the next in the order: Correlation → Mitigation → Infographic → Reporting.
Concept Demonstrated: Sequential orchestration and agent workflow management.

CorrelationAgent
Type: LlmAgent
Role: Triage and enrichment. Reads raw user alerts such as failed logins or suspicious network activity and analyzes them using historical data stored in its long-term memory.
Input: Raw user alert payload
Output: incident_report
Concept Demonstrated: Long-term memory usage in ADK

MitigationAgent
Type: LlmAgent
Role: Performs the actual security action. Interprets the incident_report and identifies the malicious IP address. Calls the custom tool BlockIPTTool to simulate blocking the IP.
Input: incident_report
Output: mitigation_status
Concept Demonstrated: Custom tool invocation

InfographicAgent
Type: LlmAgent
Role: Converts the combined incident summary and mitigation status into a visually appealing infographic for management-level viewers.
Input: incident_report and mitigation_status
Output: security_image_result (URL to generated infographic)
Concept Demonstrated: Built-in AI image generation

ReportingAgent
Type: LlmAgent
Role: Creates the final SOC report. It reads all saved session state keys: incident_report, mitigation_status, security_image_result, and the original user alerts. It synthesizes a complete text report summarizing the entire incident.
Input: All previous state keys
Output: Final text report
Concept Demonstrated: Session and state management

Agent Connectivity and Workflow Explanation

The session state acts as the communication channel between agents. Each agent reads only the keys it requires and writes its own output back to the state for the next agent to use. The SequentialAgent ensures the correct order of execution.

Step 1: CorrelationAgent
Reads: user_input
Work: Correlates and analyzes alerts using Memory Bank
Writes: state["incident_report"]

Step 2: MitigationAgent
Reads: state["incident_report"]
Work: Determines malicious IP and triggers BlockIPTool
Writes: state["mitigation_status"]

Step 3: InfographicAgent
Reads: state["incident_report"], state["mitigation_status"]
Work: Creates security infographic
Writes: state["security_image_result"]

Step 4: ReportingAgent
Reads: All previous state entries
Work: Generates complete SOC-style incident report
Returns: Final output sent to user dashboard

Flask Dashboard

A simple Flask dashboard is included to visualize:

Raw alerts

Generated incident report

Mitigation status

Infographic image

Final SOC report

This provides observability and demonstrates how multi-agent systems can be integrated into real applications.

Key Features

Fully sequential multi-agent architecture

Long-term memory for threat correlation

Custom tool for IP blocking

Automated infographic generation

End-to-end SOC-style reporting

Flask interface for visualization

Extensible modular ADK setup

Example Project Structure

project/
agents/
root_agent.py
correlation_agent.py
mitigation_agent.py
infographic_agent.py
reporting_agent.py
tools/
block_ip_tool.py
memory/
historical_threats.json
app.py (Flask dashboard)
run.py
README.md

How to Run

Install dependencies:
pip install -r requirements.txt

Start the system:
python run.py

Navigate to:
http://localhost:5000

Future Enhancements

Add anomaly detection ML model

More mitigation tools (firewall updates, user lockout)

Real-time SIEM alert ingestion

Authentication for dashboard

Enhanced memory indexing for faster correlation
