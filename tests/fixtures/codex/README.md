runtime: codex
portable_skill: .agents/skills/harness/SKILL.md
status: supported
profile: optional-native-agent
isolation: advisory-unless-worktree
communication: verified-native-channel-or-workspace-handoff
degradation: use non-overlapping ownership or serialize when isolation is unavailable
