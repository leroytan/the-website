from datetime import datetime, timezone
from unittest.mock import Mock, patch

import botocore.exceptions
import pytest
from api.logic.user_logic import UserLogic
from api.router.models import UserView
from fastapi import HTTPException


class TestUserLogic:
    """Test cases for UserLogic class"""

    @pytest.mark.unit
    @pytest.mark.logic
    @patch("api.logic.user_logic.UserLogic.get_profile_photo_url")
    def test_convert_user_to_view_success(self, mock_get_photo_url):
        """Test successful conversion of user to view"""
        # Mock user
        mock_user = Mock()
        mock_user.id = 1
        mock_user.name = "Test User"
        mock_user.email = "test@example.com"
        mock_user.intends_to_be_tutor = True
        mock_user.created_at = datetime.now(timezone.utc)
        mock_user.updated_at = datetime.now(timezone.utc)

        # Mock photo URL
        mock_get_photo_url.return_value = "https://example.com/photo.jpg"

        # Test the method
        result = UserLogic.convert_user_to_view(mock_user)

        assert isinstance(result, UserView)
        assert result.id == 1
        assert result.name == "Test User"
        assert result.email == "test@example.com"
        assert result.intends_to_be_tutor is True
        assert result.profile_photo_url == "https://example.com/photo.jpg"
        mock_get_photo_url.assert_called_once_with(1)

    @pytest.mark.unit
    @pytest.mark.logic
    @patch("api.logic.user_logic.s3_client")
    @patch("api.logic.user_logic.settings")
    @patch("api.logic.user_logic.UserLogic.get_profile_photo_url")
    def test_upload_profile_photo_success(
        self, mock_get_photo_url, mock_settings, mock_s3_client
    ):
        """Test successful profile photo upload"""
        # Mock settings
        mock_settings.r2_bucket_name = "test-bucket"

        # Mock S3 client
        mock_s3_client.put_object.return_value = None

        # Mock photo URL
        mock_get_photo_url.return_value = "https://example.com/photo.jpg"

        # Test data
        file_data = b"test_image_data"
        user_id = 1
        content_type = "image/jpeg"

        # Test the method
        result = UserLogic.upload_profile_photo(file_data, user_id, content_type)

        assert result["message"] == "Profile photo uploaded successfully"
        assert result["url"] == "https://example.com/photo.jpg"
        mock_s3_client.put_object.assert_called_once_with(
            Bucket="test-bucket",
            Key="profile_photos/1",
            Body=file_data,
            ContentType=content_type,
        )

    @pytest.mark.unit
    @pytest.mark.logic
    def test_upload_profile_photo_client_error(self):
        """Test upload_profile_photo with ClientError"""
        with patch("api.logic.user_logic.s3_client") as mock_s3:
            mock_s3.put_object.side_effect = botocore.exceptions.ClientError(
                {"Error": {"Code": "AccessDenied", "Message": "Access denied"}},
                "PutObject",
            )

            with pytest.raises(botocore.exceptions.ClientError):
                UserLogic.upload_profile_photo(b"test_data", 1, "image/jpeg")

    @pytest.mark.unit
    @pytest.mark.logic
    def test_upload_profile_photo_param_validation_error(self):
        """Test upload_profile_photo with ParamValidationError"""
        with patch("api.logic.user_logic.s3_client") as mock_s3:
            mock_s3.put_object.side_effect = botocore.exceptions.ParamValidationError(
                report="Invalid parameter"
            )

            with pytest.raises(
                ValueError, match="The parameters you provided are incorrect"
            ):
                UserLogic.upload_profile_photo(b"test_data", 1, "image/jpeg")

    @pytest.mark.unit
    @pytest.mark.logic
    @patch("api.logic.user_logic.s3_client")
    @patch("api.logic.user_logic.settings")
    def test_get_profile_photo_url_success(self, mock_settings, mock_s3_client):
        """Test successful profile photo URL retrieval"""
        # Mock settings
        mock_settings.r2_bucket_name = "test-bucket"

        # Mock S3 client
        mock_s3_client.head_object.return_value = None
        mock_s3_client.generate_presigned_url.return_value = (
            "https://example.com/photo.jpg"
        )

        # Test the method
        result = UserLogic.get_profile_photo_url(1)

        assert result == "https://example.com/photo.jpg"
        mock_s3_client.head_object.assert_called_once_with(
            Bucket="test-bucket", Key="profile_photos/1"
        )
        mock_s3_client.generate_presigned_url.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_profile_photo_url_client_error_404(self):
        """Test get_profile_photo_url with ClientError 404"""
        with patch("api.logic.user_logic.s3_client") as mock_s3:
            mock_s3.head_object.side_effect = botocore.exceptions.ClientError(
                {"Error": {"Code": "404", "Message": "Not found"}}, "HeadObject"
            )

            result = UserLogic.get_profile_photo_url(1)
            assert result == ""

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_profile_photo_url_client_error_other(self):
        """Test get_profile_photo_url with ClientError other than 404"""
        with patch("api.logic.user_logic.s3_client") as mock_s3:
            mock_s3.head_object.side_effect = botocore.exceptions.ClientError(
                {"Error": {"Code": "AccessDenied", "Message": "Access denied"}},
                "HeadObject",
            )

            with pytest.raises(botocore.exceptions.ClientError):
                UserLogic.get_profile_photo_url(1)

    @pytest.mark.unit
    @pytest.mark.logic
    def test_get_profile_photo_url_param_validation_error(self):
        """Test get_profile_photo_url with ParamValidationError"""
        with patch("api.logic.user_logic.s3_client") as mock_s3:
            mock_s3.head_object.side_effect = botocore.exceptions.ParamValidationError(
                report="Invalid parameter"
            )

            with pytest.raises(
                ValueError, match="The parameters you provided are incorrect"
            ):
                UserLogic.get_profile_photo_url(1)

    @pytest.mark.unit
    @pytest.mark.logic
    @patch("api.logic.user_logic.StorageService")
    @patch("api.logic.user_logic.UserLogic.convert_user_to_view")
    def test_get_user_by_id_success(self, mock_convert, mock_storage_service):
        """Test successful user retrieval by ID"""
        # Mock storage service
        mock_storage_service.engine = Mock()

        # Mock session
        mock_session = Mock()

        # Mock user
        mock_user = Mock()
        mock_user.id = 1
        mock_user.name = "Test User"

        # Mock session context manager
        with patch("api.logic.user_logic.Session") as mock_session_class:
            mock_session_class.return_value.__enter__.return_value = mock_session

            # Mock storage service find
            mock_storage_service.find.return_value = mock_user

            # Mock convert method
            mock_convert.return_value = UserView(
                id=1,
                name="Test User",
                email="test@example.com",
                profile_photo_url="",
                intends_to_be_tutor=False,
                created_at="",
                updated_at="",
            )

            # Test the method
            result = UserLogic.get_user_by_id(1)

            assert isinstance(result, UserView)
            mock_storage_service.find.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.logic
    @patch("api.logic.user_logic.StorageService")
    def test_get_user_by_id_not_found(self, mock_storage_service):
        """Test user retrieval for non-existent user"""
        # Mock storage service
        mock_storage_service.engine = Mock()

        # Mock session context manager
        with patch("api.logic.user_logic.Session") as mock_session_class:
            mock_session_class.return_value.__enter__.return_value = Mock()

            # Mock storage service find returning None
            mock_storage_service.find.return_value = None

            # Test the method
            with pytest.raises(HTTPException) as exc_info:
                UserLogic.get_user_by_id(999)

            assert exc_info.value.status_code == 404
            assert "User not found" in str(exc_info.value.detail)

    @pytest.mark.unit
    @pytest.mark.logic
    @patch("api.logic.user_logic.StorageService")
    @patch("api.logic.user_logic.UserLogic.convert_user_to_view")
    def test_update_user_details_success(self, mock_convert, mock_storage_service):
        """Test successful user details update"""
        # Mock storage service
        mock_storage_service.engine = Mock()

        # Mock session
        mock_session = Mock()

        # Mock user
        mock_user = Mock()
        mock_user.id = 1
        mock_user.name = "Old Name"
        mock_user.intends_to_be_tutor = False

        # Mock session context manager
        with patch("api.logic.user_logic.Session") as mock_session_class:
            mock_session_class.return_value.__enter__.return_value = mock_session

            # Mock storage service find
            mock_storage_service.find.return_value = mock_user

            # Mock convert method
            mock_convert.return_value = UserView(
                id=1,
                name="New Name",
                email="test@example.com",
                profile_photo_url="",
                intends_to_be_tutor=True,
                created_at="",
                updated_at="",
            )

            # Test the method
            result = UserLogic.update_user_details(
                1, name="New Name", intends_to_be_tutor=True
            )

            assert isinstance(result, UserView)
            assert mock_user.name == "New Name"
            assert mock_user.intends_to_be_tutor is True
            mock_session.add.assert_called_once_with(mock_user)
            mock_session.commit.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.logic
    @patch("api.logic.user_logic.StorageService")
    def test_update_user_details_not_found(self, mock_storage_service):
        """Test user details update for non-existent user"""
        # Mock storage service
        mock_storage_service.engine = Mock()

        # Mock session context manager
        with patch("api.logic.user_logic.Session") as mock_session_class:
            mock_session_class.return_value.__enter__.return_value = Mock()

            # Mock storage service find returning None
            mock_storage_service.find.return_value = None

            # Test the method
            with pytest.raises(HTTPException) as exc_info:
                UserLogic.update_user_details(999, name="New Name")

            assert exc_info.value.status_code == 404
            assert "User not found" in str(exc_info.value.detail)

    @pytest.mark.unit
    @pytest.mark.logic
    @patch("api.logic.user_logic.StorageService")
    @patch("api.logic.user_logic.UserLogic.convert_user_to_view")
    def test_update_user_details_partial_update(
        self, mock_convert, mock_storage_service
    ):
        """Test partial user details update"""
        # Mock storage service
        mock_storage_service.engine = Mock()

        # Mock session
        mock_session = Mock()

        # Mock user
        mock_user = Mock()
        mock_user.id = 1
        mock_user.name = "Old Name"
        mock_user.intends_to_be_tutor = False

        # Mock session context manager
        with patch("api.logic.user_logic.Session") as mock_session_class:
            mock_session_class.return_value.__enter__.return_value = mock_session

            # Mock storage service find
            mock_storage_service.find.return_value = mock_user

            # Mock convert method
            mock_convert.return_value = UserView(
                id=1,
                name="New Name",
                email="test@example.com",
                profile_photo_url="",
                intends_to_be_tutor=False,
                created_at="",
                updated_at="",
            )

            # Test the method - only update name
            result = UserLogic.update_user_details(1, name="New Name")

            assert isinstance(result, UserView)
            assert mock_user.name == "New Name"
            assert mock_user.intends_to_be_tutor is False  # Should remain unchanged
            mock_session.add.assert_called_once_with(mock_user)
            mock_session.commit.assert_called_once()
