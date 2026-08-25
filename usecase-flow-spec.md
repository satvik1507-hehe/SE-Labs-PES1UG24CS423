# Use-Case Flow Specification
## Problem Statement #54: Local Sports Tournament & Bracket Manager

**Use Case:** Record Match Score
**Primary Actor:** Tournament Director
**Secondary Actor:** Team Captain (receives the resulting update)
**Related Requirements:** FR-003, FR-004, FR-005, NFR-001

---

### Preconditions
- The Tournament Director is authenticated and logged into the system.
- A tournament bracket has already been generated (FR-001), and the selected match exists with a status of *Scheduled* or *In Progress*.
- Both competing teams have completed registration (FR-002).

### Postconditions
- The match record is updated with the submitted score and a timestamp.
- Standings, goal differentials, and the leaderboard are recalculated (FR-004) within the 200ms target defined in NFR-001.
- If the match is marked complete, the winning team automatically advances to its next bracket slot (FR-001).
- The updated standings and bracket are visible to Team Captains (FR-005).

---

### Main Success Scenario
1. The Tournament Director selects an active match from the live match list.
2. The Tournament Director enters or updates the score for each competing team.
3. The system validates the score format and confirms the match is in an editable state.
4. The system timestamps and saves the score update.
5. The system triggers standings recalculation (**«include» Recalculate Standings**).
6. The system updates the bracket, advancing the winning team if the match is complete.
7. The system publishes the updated standings and bracket view to Team Captains.

---

### Alternate Flow — A1: Tied Score Triggers Tiebreaker Resolution
*Branches from step 5 of the Main Success Scenario.*

5a. While recalculating standings, the system detects that two or more teams now have an equal win/loss/points record.
5b. The system invokes the **«extend» Resolve Tiebreaker** use case, applying the configured tiebreaker hierarchy in order: goal differential → head-to-head result → total points.
5c. The system assigns the final ranking based on the first criterion that differentiates the tied teams.
5d. The flow resumes at step 6 of the Main Success Scenario.

---

### Notes
- Score submissions for a match not currently *Scheduled* or *In Progress* are rejected (see FR-003 acceptance criteria).
- The 200ms recalculation target (NFR-001) applies to both the Main Success Scenario and Alternate Flow A1.
