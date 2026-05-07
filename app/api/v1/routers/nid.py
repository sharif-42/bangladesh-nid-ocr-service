from fastapi import APIRouter, status


router = APIRouter(tags=["nid"])


@router.post(
    "/extract-nid-info",
    summary="Extract fields from a Bangladesh NID image",
    status_code=status.HTTP_200_OK,    
)
def extract_nid_info():
    responses={
        status.HTTP_200_OK: {"description": "Successfully extracted NID info"}
    }
    return responses
