runtime: cursor
portable_skill: .agents/skills/harness/SKILL.md
status: supported
profile: optional-.cursor/agents-profile
isolation: advisory-unless-worktree
communication: verified-native-channel-or-workspace-handoff
degradation: use explicit non-overlap or serialize when isolation is unavailable
