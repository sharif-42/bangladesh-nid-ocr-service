from abc import ABC, abstractmethod
from app.schemas.nid import NIDInfo


class OCRService(ABC):
    @abstractmethod
    async def encode_image_to_base64(self, image_bytes: bytes) -> bytes:
        """Convert an image to base64."""

    @abstractmethod
    async def extract_nid_info(self, image_bytes: bytes, content_type: str) -> NIDInfo:
        """Extract NID fields from an image."""
