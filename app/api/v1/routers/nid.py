from fastapi import APIRouter, status, UploadFile, File, Form, HTTPException
from openai import APIError, AuthenticationError

from app.schemas.nid import NIDInfo
from app.services import OpenAINIDExtractor, LocalAINIDExtractor


router = APIRouter(tags=["nid"])


@router.post(
    "/extract-nid-info",
    summary="Extract fields from a Bangladesh NID image",
    response_model=NIDInfo,
)
async def extract_nid_info(
    image: UploadFile = File(..., description="NID image file"),
    use_local_ai: bool = Form(True, description="Use local AI instead of OpenAI"),
    is_front: bool = Form(True),
):  
    # Validate image
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only image uploads are supported.",
        )
    
    # Read Image as bytes image
    image_bytes = await image.read()
    await image.close()

    # Raise error if image is empty
    if not image_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded image is empty!!!",
        )

    # Identify Service
    service = LocalAINIDExtractor() if use_local_ai else OpenAINIDExtractor()

    # Call service
    try:
        return await service.extract_nid_info(
            image_bytes=image_bytes,
            content_type=image.content_type
        )
    except AuthenticationError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"OpenAI authentication Failed! Check your API Key.",
        ) from exc
    except APIError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"OpenAI service error: {exc}",
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )
