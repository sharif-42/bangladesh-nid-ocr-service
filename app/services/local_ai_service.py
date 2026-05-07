from app.services.interfaces import OCRService
from app.schemas.nid import NIDInfo


class LocalAINIDExtractor(OCRService):
    """
    Class-based wrapper around the local AI API to extract
    structured data from Bangladeshi National ID card images.
    """

    def __init__(self) -> None:
        pass

    def extract_nid_info(self, image: bytes) -> NIDInfo:
        pass
