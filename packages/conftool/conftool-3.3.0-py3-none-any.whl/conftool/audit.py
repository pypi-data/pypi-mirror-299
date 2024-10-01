"""Audit log module for conftool."""

import base64
import json
import logging
import logging.handlers
import socket
from dataclasses import dataclass
from datetime import datetime, timezone

from typing import Dict


@dataclass
class AuditLogEntry:
    """
    Represents an entry in the audit log.

    Attributes:
        action (str): The action performed.
        timestamp (datetime): The timestamp of the action.
        actor (str): The actor who performed the action.
        kind (str): The kind of object associated with the action.
        object (str): The object ID associated with the action.
        outcome (str): The outcome of the action. Default is "success".
    """

    action: str
    timestamp: datetime
    actor: str
    kind: str
    object: str
    outcome: str = "success"
    hostname: str = "localhost"

    def json(self):
        """
        Returns a JSON representation of the audit log entry.

        Returns:
            str: The JSON representation of the audit log entry.
        """
        # We use a structrured JSON format to make it compatible with
        # ECS standards (https://www.elastic.co/guide/en/ecs/current/index.html)
        entry = {
            "ecs.version": "1.11.0",
            "@timestamp": self.timestamp.isoformat(),
            "log.level": "info",
            "event.action": self.action,
            "event.dataset": "conftool.audit",
            "event.module": "conftool",
            "event.kind": "event",
            "event.outcome": self.outcome,
            "user.name": self.actor,
            "service.type": self.kind,
            "service.name": self.object,
            "host.hostname": self.hostname,
        }

        return json.dumps(entry)

    @staticmethod
    def from_json(entry: Dict) -> "AuditLogEntry":
        """
        Creates an AuditLogEntry from a JSON representation.

        Args:
            entry (dict): The JSON representation of the audit log entry, as a dictionary.

        Returns:
            AuditLogEntry: The audit log entry.
        """
        return AuditLogEntry(
            entry["event.action"],
            datetime.fromisoformat(entry["@timestamp"]),
            entry["user.name"],
            entry["service.type"],
            entry["service.name"],
            entry["event.outcome"],
            entry["host.hostname"],
        )


class JSONHTTPLogHandler(logging.handlers.HTTPHandler):
    """Allows logging json data via HTTP POST request in application/json format"""

    def __init__(
        self, host, url, method="POST", secure=False, credentials=None, context=None
    ) -> None:
        if method != "POST":
            raise ValueError("Only POST method is supported")
        super().__init__(host, url, method, secure, credentials, context)

    def emit(self, record):
        try:
            h = self.getConnection(self.host, self.secure)
            data = record.getMessage()
            h.putrequest("POST", self.url)
            h.putheader("Content-Type", "application/json")
            h.putheader("Content-Length", str(len(data)))
            if self.credentials:
                user, password = self.credentials
                s = (f"{user}:{password}").encode("utf-8")
                s = "Basic " + base64.b64encode(s).strip().decode("ascii")
                h.putheader("Authorization", s)
            h.endheaders()
            h.send(data.encode("utf-8"))
            h.getresponse()  # can't do anything with the result
        except Exception:
            self.handleError(record)


class AuditLog:
    """
    Represents an audit log.

    Attributes:
        logger (logging.Logger): The logger used for logging audit log entries.
    """

    def __init__(self, logger: logging.Logger) -> None:
        self.logger = logger
        self.hostname = socket.gethostname()

    def log(self, entry: AuditLogEntry) -> None:
        """
        Logs the given audit log entry.

        Args:
            entry (AuditLogEntry): The audit log entry to be logged.
        """
        json_entry = entry.json()
        self.logger.info(json_entry)


def _syslog() -> logging.Logger:
    logger = logging.getLogger("ConftoolAudit")
    logger.setLevel(logging.INFO)
    handler = logging.handlers.SysLogHandler(
        address="/dev/log", facility=logging.handlers.SysLogHandler.LOG_LOCAL0
    )
    handler.setFormatter(logging.Formatter(" %(name)s[%(process)d]: @cee: %(message)s"))
    # this sets the programname in syslog
    handler.ident = "conftool-audit"
    # we don't want to propagate the log entries to the root logger
    logger.propagate = False
    logger.addHandler(handler)
    return logger


# By default our audit log will log to syslog using the local0 facility.
# It can be filtered easily in the syslog configuration using
# "programname" and "facility".
# This can be changed by the program using the audit log.
auditlog: AuditLog = AuditLog(_syslog())


def add_conftool2git_handler(address: str) -> None:
    """
    Adds a conftool2git handler to the audit log.

    Args:
        address (str): The address of the conftool2git instance.
    """
    # No need to add a handler if the address is not set
    if not address:
        return
    handler = JSONHTTPLogHandler(address, "/auditlog")
    auditlog.logger.addHandler(handler)


def set_logger(logger: logging.Logger) -> None:
    """
    Sets the logger for the audit log.

    Args:
        logger (logging.Logger): The logger to be used for logging audit log entries.
    """
    auditlog.logger = logger


def log(action: str, actor: str, kind: str, obj: str, success: bool) -> None:
    """
    Allows logging to the main auditlog instance.

    Args:
        action (str): The action performed.
        actor (str): The actor who performed the action.
        kind (str): The kind of object associated with the action.
        obj (str): The object ID associated with the action.
        success (bool): True if the action was successful.
    """
    log_entry = AuditLogEntry(
        action,
        datetime.now(timezone.utc),
        actor,
        kind,
        obj,
        "success" if success else "failure",
        auditlog.hostname,
    )
    auditlog.log(log_entry)
