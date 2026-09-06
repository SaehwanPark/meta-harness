runtime: pi
portable_skill: .agents/skills/harness/SKILL.md
status: supported
profile: optional-extension
isolation: advisory-with-serialization
communication: parent-summary-or-pi-safe-agent-team
degradation: isolate or serialize conflicting writes when the team extension is unavailable
