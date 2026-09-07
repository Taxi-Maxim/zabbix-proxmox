"""Collector registry and dispatch."""

from typing import Type

from collectors.api import ApiCollector
from collectors.backup import BackupCollector
from collectors.certificates import CertificatesCollector
from collectors.journal import JournalCollector
from collectors.services import ServicesCollector
from collectors.smart import SmartCollector
from collectors.storage import StorageCollector
from collectors.updates import UpdatesCollector
from collectors.zfs import ZfsCollector
from core.collector import Collector


COLLECTORS: dict[str, Type[Collector]] = {
    "api": ApiCollector,
    "backup": BackupCollector,
    "certificates": CertificatesCollector,
    "journal": JournalCollector,
    "services": ServicesCollector,
    "smart": SmartCollector,
    "storage": StorageCollector,
    "updates": UpdatesCollector,
    "zfs": ZfsCollector,
}


def create(name: str) -> Collector:
    """Create the requested collector."""
    return COLLECTORS[name]()