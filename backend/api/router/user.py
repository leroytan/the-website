import botocore
from api.config import settings
from api.router.auth_utils import RouterAuthUtils
from api.storage.models import User
from api.storage.object_storage import s3_client
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

router = APIRouter()

@router.post("/api/user/upload-profile-photo/")
async def upload_profile_photo(file: UploadFile = File(...), user: User = Depends(RouterAuthUtils.get_current_user)):
    if file.content_type not in ["image/jpeg", "image/png", "image/webp", "image/jpg", "image/gif"]:
        raise HTTPException(status_code=400, detail="Invalid image type")
    
    try:
        # Read file into memory
        file_data = await file.read()

        # Define the object name in the bucket
        object_key = f"profile_photos/{user.id}"

        # Upload to R2
        s3_client.put_object(
            Bucket=settings.r2_bucket_name,
            Key=object_key,
            Body=file_data,
            ContentType=file.content_type
        )

        # Return R2 object path or URL (optional)
        return {
            "message": "Profile photo uploaded successfully"
        }

    except botocore.exceptions.ClientError as error:
        # Put your error handling logic here
        raise error

    except botocore.exceptions.ParamValidationError as error:
        raise ValueError('The parameters you provided are incorrect: {}'.format(error))
    
@router.get("/api/user/profile-photo/{user_id}")
async def get_profile_photo(user_id: str):
    try:
        # Define the object name in the bucket
        object_key = f"profile_photos/{user_id}"

        # Generate a pre-signed URL for the object
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': settings.r2_bucket_name, 'Key': object_key},
            ExpiresIn=3600  # URL expiration time in seconds
        )

        return {
            "url": url
        }

    except botocore.exceptions.ClientError as error:
        # Put your error handling logic here
        raise error

    except botocore.exceptions.ParamValidationError as error:
        raise ValueError('The parameters you provided are incorrect: {}'.format(error))
    