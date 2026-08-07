---
name: stack-bootstrap
description: Bootstrap the smallest VenturaVoice Python structure for the approved speech or audio MVP using only declared stack needs. Use when the repository is ready to move from incubation docs to executable code. Do not use when a functional project structure already exists or the task is only product scoping.
---

# Stack bootstrap

- Confirm the approved voice MVP before adding dependencies.
- Add only packages required by the first executable audio path.
- Separate application code tests and small licensed audio fixtures.
- Keep model weights recordings and generated audio out of Git unless explicitly suitable for versioning.
- Add one deterministic smoke test.
- Document model language hardware and local run assumptions.
- Reuse the shared repository CI standard.
