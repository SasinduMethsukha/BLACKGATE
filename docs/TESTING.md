# Testing

- Build with `docker compose up --build`.
- Confirm the portal loads at localhost:8080.
- Confirm Stage 1 is unlocked and later stages are locked.
- Solve stages 1–5 from their supplied artefacts.
- Submit flags sequentially.
- Verify incorrect flags are rejected.
- Verify later flags are rejected until prerequisites are complete.
- Verify reset clears progress.
- Verify Stage 6 is not published to the host (`docker compose ps`).
- Rebuild from clean containers and repeat.
