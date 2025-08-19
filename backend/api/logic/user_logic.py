import botocore
from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.config import settings
from api.router.models import UserView
from api.storage.models import User
from api.storage.object_storage import s3_client
from api.storage.storage_service import StorageService


class UserLogic:
    @staticmethod
    def convert_user_to_view(user: User) -> UserView:
        """
        Converts a User object to a dictionary view.
        :param user: User object
        :return: Dictionary view of the user
        """
        photo_url = UserLogic.get_profile_photo_url(user.id)

        return UserView(
            id=user.id,
            name=user.name,
            email=user.email,
            profile_photo_url=photo_url,
            intends_to_be_tutor=user.intends_to_be_tutor,
            created_at=user.created_at.isoformat(),
            updated_at=user.updated_at.isoformat(),
        )

    @staticmethod
    def upload_profile_photo(file_data: bytes, user_id: int, content_type: str) -> None:
        try:
            # Define the object name in the bucket
            object_key = f"profile_photos/{user_id}"

            # Upload to R2
            s3_client.put_object(
                Bucket=settings.r2_bucket_name,
                Key=object_key,
                Body=file_data,
                ContentType=content_type,
            )

            # Return R2 object path or URL (optional)
            return {
                "message": "Profile photo uploaded successfully",
                "url": UserLogic.get_profile_photo_url(user_id),
            }

        except botocore.exceptions.ClientError as error:
            # Put your error handling logic here
            raise error

        except botocore.exceptions.ParamValidationError as error:
            raise ValueError(
                "The parameters you provided are incorrect: {}".format(error)
            )

    @staticmethod
    def get_profile_photo_url(user_id: int) -> str:
        try:
            # Define the object name in the bucket
            object_key = f"profile_photos/{user_id}"

            # Check if the object exists
            s3_client.head_object(Bucket=settings.r2_bucket_name, Key=object_key)

            # Generate a pre-signed URL for the object
            url = s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": settings.r2_bucket_name, "Key": object_key},
                ExpiresIn=3600,  # URL expiration time in seconds
            )
            return url
        except botocore.exceptions.ClientError as error:
            if error.response["Error"]["Code"] == "404":
                return ""
            else:
                raise error
        except botocore.exceptions.ParamValidationError as error:
            raise ValueError(
                "The parameters you provided are incorrect: {}".format(error)
            )

    @staticmethod
    def get_user_by_id(user_id: int) -> UserView:
        with Session(StorageService.engine) as session:
            user = StorageService.find(session, {"id": user_id}, User, find_one=True)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return UserLogic.convert_user_to_view(user)

    @staticmethod
    def update_user_details(
        user_id: int, name: str | None = None, intends_to_be_tutor: bool | None = None
    ) -> UserView:
        with Session(StorageService.engine) as session:
            user = StorageService.find(session, {"id": user_id}, User, find_one=True)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            if name is not None:
                user.name = name
            if intends_to_be_tutor is not None:
                user.intends_to_be_tutor = intends_to_be_tutor

            session.add(user)
            session.commit()
            session.refresh(user)
            return UserLogic.convert_user_to_view(user)
