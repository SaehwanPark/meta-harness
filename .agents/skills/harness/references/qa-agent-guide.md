# QA Specialist Guide

Use a reusable QA brief or skill when a recurring integration risk warrants independent review. For an ordinary check, use the same criteria in the main workflow.

Compare the real producer and consumer using the original request and acceptance criteria. For an API, compare an actual response or contract test against the parser and types, including nullability and nesting. For routes, resolve links against the real path and deployment prefix. For state transitions, trace allowed transitions through the code and exercise the ones that can strand a run.

Report the evidence, impact, and smallest fix for each concrete mismatch. Identify unverified boundaries. Return findings to the owner and persist them only when a later consumer needs the evidence.
