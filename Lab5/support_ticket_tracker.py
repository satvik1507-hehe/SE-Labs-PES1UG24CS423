"""A small in-memory support ticket tracker with JSON persistence."""

import json
import logging
from pathlib import Path
from typing import Any

Ticket = dict[str, Any]
TICKETS: dict[str, Ticket] = {}
LOGGER = logging.getLogger(__name__)


def create_ticket(
    title: str,
    description: str,
    reporter: str,
    priority: str = "medium",
    category: str = "general",
    audit_log: list[str] | None = None,
) -> Ticket | None:
    """Create a ticket and optionally append an audit entry."""
    if not title.strip():
        return None

    ticket_id = str(len(TICKETS) + 1)
    ticket: Ticket = {
        "id": ticket_id,
        "title": title,
        "description": description,
        "priority": priority,
        "category": category,
        "status": "open",
        "reporter": reporter,
        "assignee": None,
    }
    TICKETS[ticket_id] = ticket
    if audit_log is not None:
        audit_log.append(f"Created ticket {ticket_id} for {reporter}")
    return ticket


def assign_ticket(ticket_id: str, agent: str, notify: bool = False) -> bool:
    """Assign a ticket; return False when the ticket does not exist."""
    del notify  # Reserved for a future notification integration.
    ticket = TICKETS.get(ticket_id)
    if ticket is None:
        return False
    ticket["assignee"] = agent
    return True


def update_status(ticket_id: str, status: str) -> Ticket | None:
    """Update a ticket's status, returning None for an unknown ID."""
    ticket = TICKETS.get(ticket_id)
    if ticket is None:
        return None
    ticket["status"] = status
    return ticket


def search_tickets(
    status: str | None = None, priority: str | None = None
) -> list[Ticket]:
    """Return tickets matching any provided filters."""
    return [
        ticket
        for ticket in TICKETS.values()
        if (status is None or ticket["status"] == status)
        and (priority is None or ticket["priority"] == priority)
    ]


def save_tickets(path: str | Path = "tickets.json") -> None:
    """Save tickets as readable JSON."""
    with Path(path).open("w", encoding="utf-8") as ticket_file:
        json.dump(TICKETS, ticket_file, indent=2)


def load_tickets(path: str | Path = "tickets.json") -> None:
    """Load tickets from JSON, replacing the current in-memory collection."""
    global TICKETS
    with Path(path).open("r", encoding="utf-8") as ticket_file:
        loaded_tickets = json.load(ticket_file)
    if not isinstance(loaded_tickets, dict):
        raise ValueError("Ticket data must be a JSON object")
    TICKETS = loaded_tickets


def print_ticket_report() -> None:
    """Print a compact summary of all tickets."""
    print("Support Tickets")
    if not TICKETS:
        print("No tickets yet")
        return
    for ticket_id, ticket in TICKETS.items():
        print(ticket_id, ticket["title"], ticket["status"])


def close_ticket(ticket_id: str) -> bool:
    """Close a ticket; return False when its ID is unknown."""
    ticket = TICKETS.get(ticket_id)
    if ticket is None:
        return False
    ticket["status"] = "closed"
    return True


def is_open(ticket_id: str) -> bool:
    """Return whether a ticket is open or in progress."""
    ticket = TICKETS.get(ticket_id)
    return ticket is not None and ticket["status"] in {"open", "in_progress"}


def main() -> None:
    """Run a short interactive demonstration of the tracker."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    TICKETS.clear()
    create_ticket("Cannot sign in", "Password reset link fails", "alex@example.com")
    create_ticket("Billing question", "Charged twice", "lee@example.com", "high")
    assign_ticket("1", "agent-01")
    update_status("1", "in_progress")
    print_ticket_report()
    LOGGER.info("Tickets created: %d", len(TICKETS))
    print("Ticket 1 open?", is_open("1"))

    ticket_id = input("Ticket id to close (Enter to skip): ").strip()
    if ticket_id and not close_ticket(ticket_id):
        print(f"Ticket {ticket_id} was not found")
    save_tickets()


if __name__ == "__main__":
    main()
