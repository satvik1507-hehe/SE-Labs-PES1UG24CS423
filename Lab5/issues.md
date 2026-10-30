# Static analysis issue log

Line numbers refer to the original `support_ticket_tracker.py` in the assigned repository (89 lines).

| Issue | Type | Line(s) | Description | Fix approach |
|---|---|---:|---|---|
| Unsafe `eval` call | Security / Bandit high | 85 | Evaluates a string as Python code, creating an unnecessary code-execution risk. | Removed the unsafe demo and its environment-variable switch. |
| Mutable default argument | Bug / Pylint | 8, 14 | Every call without an explicit audit log shares the same list object. | Use `None` as the default; append only when the caller supplies a list. |
| Bare `except` and silent failure | Reliability / Pylint | 18–23 | Hides every exception and makes debugging impossible when assignment fails. | Use `dict.get`; return `False` for a missing ticket. |
| Unclosed file handles | Reliability / Pylint | 42–50 | Files may remain open if reading or writing raises an error. | Use `with` blocks and UTF-8 encoding for JSON files. |
| Nullable comparison/style issue | Style / Flake8 | 33 | `status != None` does not follow Python's identity check convention. | Use `status is None` in the filter condition. |
| Unused imports and local | Style / Pylint, Flake8 | 3–5, 77 | `sys`, `random`, and `count` are unused. | Remove unused names and log the actual ticket count directly. |
| Unsafe direct dictionary indexing | Bug | 27, 62, 65 | Unknown ticket IDs raise `KeyError`; the sample prompts for an ID but does not handle an unknown ID. | Use `.get()` and return a clear failure result for unknown IDs. |
| Non-PEP 8 function name and formatting | Style / Pylint, Flake8 | 12, 61 | `closeTicket` is not snake_case; long dictionary construction is difficult to read. | Rename to `close_ticket` and format the ticket fields across multiple lines. |

## Verification status

The fixes are present in the cleaned script. Pylint, Bandit, and Flake8 were not installed in the available environment, and outbound package access is unavailable, so analyzer-generated before/after reports and the requested Pylint score still need to be produced on a machine with those tools installed. Do not submit invented analyzer output as if the tools ran.
