# Lab 5 reflection

The Lab 5 handout lists reflection as a deliverable but does not include reflection questions. These answers reflect on the static analysis work and the Lab 2 reflection prompts are answered separately in `jira-lab-guide.md`.

1. **Which issue mattered most?** The `eval` call was the highest-risk issue because it executes code and was only present in an optional demo. Removing the demo eliminated the risk without changing the tracker’s intended behavior.
2. **Which fixes improved reliability?** Replacing the shared mutable default, safely handling unknown IDs, and using context managers for files made behavior more predictable and failures easier to understand.
3. **What did the tools contribute?** Pylint can identify maintainability and correctness concerns, Flake8 catches formatting violations, and Bandit focuses on risky security patterns. Their reports guide a review; each finding still needs context before changing code.
4. **What remains to complete?** Run Pylint, Bandit, and Flake8 before and after changes, preserve the actual report files, and confirm the final Pylint score is above 9.5. The analyzer packages were unavailable in this environment, so no score or clean-report claim is made here.
