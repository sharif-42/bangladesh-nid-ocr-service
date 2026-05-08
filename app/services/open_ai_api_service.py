import json
import base64

from openai import AsyncOpenAI

from app.services.interfaces import OCRService
from app.schemas.nid import NIDInfo
from app.core.config import settings

from app.utils.utils import NID_OCR_PROMT


class OpenAINIDExtractor(OCRService):
    """
    Class-based wrapper around the OpenAI Responses API to extract
    structured data from Bangladeshi National ID card images.
    """

    def __init__(self) -> None:
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL
        self.client = AsyncOpenAI(
            api_key=self.api_key,
            timeout=settings.REQUEST_TIMEOUT_SECONDS
        )
        self.prompt = NID_OCR_PROMT

    async def encode_image_to_base64(self, image_bytes: bytes) -> bytes:
        return base64.b64encode(image_bytes).decode("utf-8")

    async def extract_nid_info(self, image_bytes: bytes, content_type: str) -> NIDInfo:
        """
            High-level API: given a local image path, return parsed JSON
            with NID fields.
        """
        base64_image = await self.encode_image_to_base64(image_bytes)

        # Call the OPEN API model
        completion = await self.client.chat.completions.create(
            model=self.model,
            response_format={"type": "json_object"},
            messages = [
                {
                    "role": "system",
                    "content": self.prompt,
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Extract NID information from this image."
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:{content_type};base64,{base64_image}"},
                        }
                    ]
                }
            ]
        )

        content = completion.choices[0].message.content       
        parsed_data = json.loads(content)

        try:
            return NIDInfo.model_validate(parsed_data)
        except ValidationError as exc:
            raise ValueError(f"Failed to parse NID info: {exc}") from exc
