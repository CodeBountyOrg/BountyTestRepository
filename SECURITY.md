# Security guardrail

Issue #9 reports `xyz.dll` as a vulnerable artifact. This repository should not ship or reference that DLL.

Run the repository security guard before submitting changes:

```bash
npm run security:audit
```

The audit checks tracked source paths and filenames for blocked artifacts listed in `security/denylist.json` so the vulnerable DLL cannot be reintroduced silently.
