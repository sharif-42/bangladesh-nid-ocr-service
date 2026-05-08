from app.services.interfaces import OCRService
from app.schemas.nid import NIDInfo


class LocalAINIDExtractor(OCRService):
    """
    Class-based wrapper around the local AI API to extract
    structured data from Bangladeshi National ID card images.
    """

    def __init__(self) -> None:
        pass

    async def encode_image_to_base64(self, image_bytes: bytes) -> bytes:
        return base64.b64encode(image_bytes).decode("utf-8")

    async def extract_nid_info(self, image_bytes: bytes, content_type: str) -> NIDInfo:
        return {}

