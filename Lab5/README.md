# Lab 5: Static Code Analysis

This folder contains the cleaned support ticket tracker, the issue log, and reflection answers.

## Generate the required analyzer reports

The Pylint, Bandit, and Flake8 packages were unavailable in the preparation environment, so report files and a Pylint score have not been fabricated. In a Python environment with internet access, run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pylint bandit flake8
```

Run each tool against the original starter script before replacing it, and save the output as `pylint_report_before.txt`, `bandit_report_before.txt`, and `flake8_report_before.txt`. Then run the same commands against the cleaned `support_ticket_tracker.py` and save the results as `pylint_report_after.txt`, `bandit_report_after.txt`, and `flake8_report_after.txt`.

Commands for the cleaned file:

```bash
python -m pylint support_ticket_tracker.py > pylint_report_after.txt
python -m bandit -r support_ticket_tracker.py > bandit_report_after.txt
python -m flake8 support_ticket_tracker.py > flake8_report_after.txt
```

The Lab 5 handout asks for three commits, one per tool. Keep the report results genuine and use the actual findings when preparing those commits. The clean script was compiled and run through its demonstration flow during preparation; analyzer verification remains outstanding.
