# Lab 1 — Requirements Table
## Problem Statement #54: Local Sports Tournament & Bracket Manager

**Stakeholders / Actors:** Team Captain, Tournament Director

---

## Functional Requirements

| ID | Type | Description | Priority | Acceptance Criteria | Rationale |
|----|------|-------------|----------|----------------------|-----------|
| FR-001 | Functional | The system shall automatically generate seeded single/double-elimination tournament brackets based on initial team rankings entered by the Tournament Director. | High | **Pass:** Winner of Match 1 advances automatically to the correct slot in Match 2. **Fail:** Bracket produces invalid or duplicate match pairings. | Manual bracket seeding is slow and error-prone; automated seeding guarantees a fair, reproducible bracket structure. |
| FR-002 | Functional | The system shall allow a Team Captain to register their team and submit a player roster before the registration deadline. | High | **Pass:** Registered team appears in the Tournament Director's team list with a roster count greater than zero. **Fail:** A roster submitted after the deadline is accepted, or duplicate team names are allowed. | Accurate rosters are required for eligibility checks, seeding, and bracket generation. |
| FR-003 | Functional | The system shall allow the Tournament Director to record live match scores for each scheduled match, including in-progress updates. | High | **Pass:** A submitted score is timestamped and reflected on the match's live score display within 2 seconds. **Fail:** A score submission is accepted for a match that is not currently scheduled or in progress. | Real-time score capture is the core trigger for standings recalculation and spectator engagement. |
| FR-004 | Functional | The system shall automatically compute tiebreakers (e.g., goal differential, head-to-head result, points) whenever two or more teams have an equal win/loss/points record. | High | **Pass:** Standings order tied teams according to the configured tiebreaker hierarchy and match the expected ranking. **Fail:** Tied teams are left in an ambiguous or non-deterministic order. | Consistent tiebreak rules are essential to tournament fairness; manual resolution is inconsistent and disputable. |
| FR-005 | Functional | The system shall publish updated league standings and bracket status to a public-facing view accessible to Team Captains after every recorded match. | Medium | **Pass:** The standings page reflects the latest match result within the NFR-001 latency target. **Fail:** Standings shown to captains differ from the Director's internal record. | Transparent, up-to-date standings maintain stakeholder trust and reduce support/dispute requests. |

---

## Non-Functional Requirements

| ID | Type | Description | Priority | Acceptance Criteria | Rationale |
|----|------|-------------|----------|----------------------|-----------|
| NFR-001 | Performance & Security | Standings, goal differentials, and the tournament leaderboard must recalculate within 200ms of score submission, and all score-submission endpoints must be authenticated and encrypted in transit. | High | **Pass:** Benchmarking confirms <200ms recalculation latency and TLS-secured, authenticated score submission under simulated peak load. **Fail:** Latency exceeds 200ms, or unauthenticated writes to match scores are possible. | Live tournaments need near-real-time feedback for spectators, and score data integrity must be protected from tampering. |
| NFR-002 | Usability & Reliability | The bracket and standings views shall be responsive on mobile devices, and the system shall maintain 99.5% uptime during active tournament days. | Medium | **Pass:** Usability testing confirms all core views render correctly on screens ≥360px wide, and uptime logs show ≥99.5% availability during tournament hours. **Fail:** Layout breaks on mobile, or downtime exceeds 0.5% during active tournament hours. | Captains and spectators primarily check live scores on phones; downtime during matches directly damages tournament credibility. |
