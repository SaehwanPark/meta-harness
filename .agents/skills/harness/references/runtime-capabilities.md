# Runtime Capabilities

When adapting a portable role, verify only the capabilities required by the workflow, such as skill discovery, spawning, workspace isolation, resource enforcement, communication, durable state, permissions, model routing, or lifecycle control.

| Status | Meaning |
| --- | --- |
| `supported` | The selected deployment provides the guarantee |
| `supported_with_extension` | A selected optional integration provides it |
| `advisory` | The runtime can express intent without enforcing the guarantee |
| `unsupported` | The workflow needs a fallback |

For conflicting writes or test state, prefer runtime enforcement or an isolated workspace. Explicit non-overlap is suitable when the workflow can safely operate on separate resources. Serialize work that would conflict, and report a blocker if the required guarantee still cannot be met.

Match communication to its lifetime. Use verified native messaging for ephemeral results. Use durable runtime state or a deterministic workspace artifact when another session must inspect or resume the work. Surface unavailable capabilities and missing required results.

Inherit model and settings by default. A portable role can express a material requirement with `inherit`, `fast`, `economy`, `balanced`, or `strong`. Map that intent in a removable profile if the runtime exposes the controls. Keep skill and role contracts usable after profile removal.
