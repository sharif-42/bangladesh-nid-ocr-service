from pydantic import BaseModel, Field
from fastapi import UploadFile


class NIDExtractionRequest(BaseModel):
    image: UploadFile | None = Field(None, description="NID card image")
    is_front: bool = Field(
        default=True,
        description="Use this parameter if the image is of the front side of the NID card. By default, it is set to True. If the image is of the back side of the NID card, set this parameter to False."
    )
    use_local_ai: bool = Field(
        default=True,
        description="Use local AI for NID card extraction. By default, it is set to True. If you want to use OpenAI for NID card extraction, set this parameter to False."
    )


class NIDInfo(BaseModel):
    name_bn: str | None = Field(default="", description="Name in Bangla")
    name_en: str | None = Field(default="", description="Name in English")
    father_name_bn: str | None = Field(default="", description="Father's name")
    mother_name_bn: str | None = Field(default="", description="Mother's name")
    date_of_birth: str | None = Field(default="", description="Date of birth")
    nid_number: str | None = Field(default="", description="NID number")
