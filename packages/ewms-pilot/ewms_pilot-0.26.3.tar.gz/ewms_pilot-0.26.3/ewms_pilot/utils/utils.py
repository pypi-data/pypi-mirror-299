"""Common utilities."""

import logging

LOGGER = logging.getLogger(__name__)


def all_task_errors_string(task_errors: list[BaseException]) -> str:
    """Make a string from the multiple task exceptions."""
    for exception in task_errors:
        LOGGER.error(exception)
    return (
        f"{len(task_errors)} TASK(S) FAILED: "
        f"{', '.join(repr(e) for e in task_errors)}"
    )
