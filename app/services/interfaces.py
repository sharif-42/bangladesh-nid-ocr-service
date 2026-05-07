from abc import ABC, abstractmethod
from typing import Any

from app.schemas.nid import NIDInfo


class OCRService(ABC):
    @abstractmethod
    def extract_nid_info(self, image: bytes) -> NIDInfo:
        """Extract NID fields from an image."""
