# BLACKGATE — Operation Nightfall

Complete local educational CTF box for IE3132 Penetration Testing Assignment 01.

## Start
```bash
docker compose up --build
```
Then open `http://localhost:8080`.

## Stages
1. OSINT — The Public Trail
2. Steganography — Pixels Don't Lie
3. Cryptography — Lazy Transmission
4. Digital Forensics — The Quiet Log
5. Networking — Packets in the Dark
6. Web Security — The Blackgate Gate

## Reset
Use the portal reset button or recreate the containers:
```bash
docker compose down
docker compose up --build --force-recreate
```

## Safety
Stage 6 is intentionally vulnerable. It is not published to the host and the Docker network is internal. Do not expose the project publicly. All challenge data is fictional/synthetic.
