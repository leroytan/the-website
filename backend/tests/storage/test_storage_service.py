import pytest
from unittest.mock import Mock, patch, MagicMock
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import Session
from fastapi import HTTPException

from api.storage.storage_service import StorageService
from api.storage.models import User, Assignment
from api.exceptions import TableEmptyError


class TestStorageService:
    """Tests for StorageService"""

    @pytest.mark.unit
    @pytest.mark.storage
    def test_init_db_database_exists(self):
        """Test database initialization when database exists"""
        mock_engine = Mock()
        mock_engine.url = "sqlite:///test.db"
        
        with patch('api.storage.storage_service.database_exists') as mock_exists:
            with patch('api.storage.storage_service.inspect') as mock_inspect:
                with patch('api.storage.storage_service.Base') as mock_base:
                    with patch('api.storage.storage_service.Session') as mock_session:
                        with patch('api.storage.storage_service.seed_database') as mock_seed:
                            with patch('api.storage.storage_service.settings') as mock_settings:
                                with patch('api.storage.storage_service.insert_test_data') as mock_insert:
                                    # Mock database exists and has tables
                                    mock_exists.return_value = True
                                    mock_inspect.return_value.get_table_names.return_value = ['users', 'assignments']
                                    mock_settings.db_populate_check = False
                                    
                                    StorageService.init_db(mock_engine)
                                    
                                    # Verify engine was set
                                    assert StorageService.engine == mock_engine

    @pytest.mark.unit
    @pytest.mark.storage
    def test_init_db_create_database(self):
        """Test database initialization when database doesn't exist"""
        mock_engine = Mock()
        mock_engine.url = "sqlite:///test.db"
        
        with patch('api.storage.storage_service.database_exists') as mock_exists:
            with patch('api.storage.storage_service.create_database') as mock_create:
                with patch('api.storage.storage_service.inspect') as mock_inspect:
                    with patch('api.storage.storage_service.Base') as mock_base:
                        with patch('api.storage.storage_service.Session') as mock_session:
                            with patch('api.storage.storage_service.seed_database') as mock_seed:
                                with patch('api.storage.storage_service.settings') as mock_settings:
                                    with patch('api.storage.storage_service.insert_test_data') as mock_insert:
                                        # Mock database doesn't exist
                                        mock_exists.return_value = False
                                        mock_inspect.return_value.get_table_names.return_value = []
                                        mock_settings.db_populate_check = False
                                        
                                        StorageService.init_db(mock_engine)
                                        
                                        # Verify database was created
                                        mock_create.assert_called_once_with(mock_engine.url)
                                        assert StorageService.engine == mock_engine

    @pytest.mark.unit
    @pytest.mark.storage
    def test_init_db_with_populate(self):
        """Test database initialization with test data population"""
        mock_engine = Mock()
        mock_engine.url = "sqlite:///test.db"
        
        with patch('api.storage.storage_service.database_exists') as mock_exists:
            with patch('api.storage.storage_service.inspect') as mock_inspect:
                with patch('api.storage.storage_service.Base') as mock_base:
                    with patch('api.storage.storage_service.Session') as mock_session:
                        with patch('api.storage.storage_service.seed_database') as mock_seed:
                            with patch('api.storage.storage_service.settings') as mock_settings:
                                with patch('api.storage.storage_service.insert_test_data') as mock_insert:
                                    # Mock database doesn't exist (to trigger the populate path)
                                    mock_exists.return_value = False
                                    mock_inspect.return_value.get_table_names.return_value = []
                                    mock_settings.db_populate_check = True
                                    mock_insert.return_value = True
                                    
                                    StorageService.init_db(mock_engine)
                                    
                                    # Verify test data was inserted
                                    mock_insert.assert_called_once_with(mock_engine)

    @pytest.mark.unit
    @pytest.mark.storage
    def test_find_with_dict_query(self):
        """Test find method with dictionary query"""
        mock_session = Mock()
        mock_user = Mock(spec=User)
        mock_user.id = 1
        mock_user.email = "test@example.com"
        
        with patch('api.storage.storage_service.Session') as mock_session_class:
            with patch('api.storage.storage_service.select') as mock_select:
                with patch('api.storage.storage_service.StorageService.engine') as mock_engine:
                    # Mock session and query execution
                    mock_session_instance = Mock()
                    mock_session_class.return_value.__enter__.return_value = mock_session_instance
                    mock_statement = Mock()
                    mock_select.return_value = mock_statement
                    mock_statement.filter_by.return_value = mock_statement
                    mock_session_instance.execute.return_value.scalars.return_value.all.return_value = [mock_user]
                    
                    result = StorageService.find(mock_session, {"email": "test@example.com"}, User)
                    
                    assert result == [mock_user]
                    mock_statement.filter_by.assert_called_once_with(email="test@example.com")

    @pytest.mark.unit
    @pytest.mark.storage
    def test_find_with_list_query(self):
        """Test find method with list query"""
        mock_session = Mock()
        mock_user = Mock(spec=User)
        mock_user.id = 1
        mock_user.email = "test@example.com"
        
        with patch('api.storage.storage_service.Session') as mock_session_class:
            with patch('api.storage.storage_service.select') as mock_select:
                with patch('api.storage.storage_service.and_') as mock_and:
                    with patch('api.storage.storage_service.StorageService.engine') as mock_engine:
                        # Mock session and query execution
                        mock_session_instance = Mock()
                        mock_session_class.return_value.__enter__.return_value = mock_session_instance
                        mock_statement = Mock()
                        mock_select.return_value = mock_statement
                        mock_statement.where.return_value = mock_statement
                        mock_session_instance.execute.return_value.scalars.return_value.all.return_value = [mock_user]
                        
                        # Create a mock column element
                        mock_column = Mock()
                        query_list = [mock_column]
                        
                        result = StorageService.find(mock_session, query_list, User)
                        
                        assert result == [mock_user]
                        mock_statement.where.assert_called_once_with(mock_and.return_value)

    @pytest.mark.unit
    @pytest.mark.storage
    def test_find_with_query_object(self):
        """Test find method with Query object"""
        mock_session = Mock()
        mock_user = Mock(spec=User)
        mock_user.id = 1
        mock_user.email = "test@example.com"
        
        # Create a proper Query mock
        from sqlalchemy.orm import Query
        mock_query = Mock(spec=Query)
        
        with patch('api.storage.storage_service.Session') as mock_session_class:
            with patch('api.storage.storage_service.StorageService.engine') as mock_engine:
                # Mock session and query execution
                mock_session_instance = Mock()
                mock_session_class.return_value.__enter__.return_value = mock_session_instance
                mock_session_instance.execute.return_value.scalars.return_value.all.return_value = [mock_user]
                
                result = StorageService.find(mock_session, mock_query, User)
                
                assert result == [mock_user]
                mock_session_instance.execute.assert_called_once_with(mock_query)

    @pytest.mark.unit
    @pytest.mark.storage
    def test_find_find_one_true(self):
        """Test find method with find_one=True"""
        mock_session = Mock()
        mock_user = Mock(spec=User)
        mock_user.id = 1
        mock_user.email = "test@example.com"
        
        with patch('api.storage.storage_service.Session') as mock_session_class:
            with patch('api.storage.storage_service.select') as mock_select:
                with patch('api.storage.storage_service.StorageService.engine') as mock_engine:
                    # Mock session and query execution
                    mock_session_instance = Mock()
                    mock_session_class.return_value.__enter__.return_value = mock_session_instance
                    mock_statement = Mock()
                    mock_select.return_value = mock_statement
                    mock_statement.filter_by.return_value = mock_statement
                    mock_session_instance.execute.return_value.scalars.return_value.first.return_value = mock_user
                    
                    result = StorageService.find(mock_session, {"email": "test@example.com"}, User, find_one=True)
                    
                    assert result == mock_user
                    mock_session_instance.execute.return_value.scalars.return_value.first.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.storage
    def test_find_invalid_query_type(self):
        """Test find method with invalid query type"""
        mock_session = Mock()
        
        with pytest.raises(ValueError, match="Query must be a dictionary or a list of ColumnElement objects"):
            StorageService.find(mock_session, "invalid_query", User)

    @pytest.mark.unit
    @pytest.mark.storage
    def test_find_empty_result_with_empty_query(self):
        """Test find method with empty result and empty query"""
        mock_session = Mock()
        
        with patch('api.storage.storage_service.Session') as mock_session_class:
            with patch('api.storage.storage_service.select') as mock_select:
                with patch('api.storage.storage_service.StorageService.engine') as mock_engine:
                    with patch('api.storage.storage_service.Utils') as mock_utils:
                        # Mock session and empty result
                        mock_session_instance = Mock()
                        mock_session_class.return_value.__enter__.return_value = mock_session_instance
                        mock_statement = Mock()
                        mock_select.return_value = mock_statement
                        mock_statement.filter_by.return_value = mock_statement
                        mock_session_instance.execute.return_value.scalars.return_value.all.return_value = []
                        
                        # Mock Utils to raise ValueError for empty query
                        mock_utils.validate_non_empty.side_effect = ValueError("Empty query")
                        
                        with pytest.raises(TableEmptyError):
                            StorageService.find(mock_session, {}, User)

    @pytest.mark.unit
    @pytest.mark.storage
    def test_find_any_with_multiple_queries(self):
        """Test find_any method with multiple queries"""
        mock_session = Mock()
        mock_user = Mock(spec=User)
        mock_user.id = 1
        mock_user.email = "test@example.com"
        
        with patch('api.storage.storage_service.Session') as mock_session_class:
            with patch('api.storage.storage_service.select') as mock_select:
                with patch('api.storage.storage_service.and_') as mock_and:
                    with patch('api.storage.storage_service.or_') as mock_or:
                        with patch('api.storage.storage_service.StorageService.engine') as mock_engine:
                            # Mock session and query execution
                            mock_session_instance = Mock()
                            mock_session_class.return_value.__enter__.return_value = mock_session_instance
                            mock_statement = Mock()
                            mock_select.return_value = mock_statement
                            mock_statement.where.return_value = mock_statement
                            mock_session_instance.execute.return_value.scalars.return_value.all.return_value = [mock_user]
                            
                            queries = [{"email": "test@example.com"}, {"id": 1}]
                            
                            result = StorageService.find_any(mock_session, queries, User)
                            
                            assert result == [mock_user]
                            mock_statement.where.assert_called_once_with(mock_or.return_value)

    @pytest.mark.unit
    @pytest.mark.storage
    def test_find_any_empty_result(self):
        """Test find_any method with empty result"""
        mock_session = Mock()
        
        with patch('api.storage.storage_service.Session') as mock_session_class:
            with patch('api.storage.storage_service.select') as mock_select:
                with patch('api.storage.storage_service.and_') as mock_and:
                    with patch('api.storage.storage_service.or_') as mock_or:
                        with patch('api.storage.storage_service.StorageService.engine') as mock_engine:
                            with patch('api.storage.storage_service.Utils') as mock_utils:
                                # Mock session and empty result
                                mock_session_instance = Mock()
                                mock_session_class.return_value.__enter__.return_value = mock_session_instance
                                mock_statement = Mock()
                                mock_select.return_value = mock_statement
                                mock_statement.where.return_value = mock_statement
                                mock_session_instance.execute.return_value.scalars.return_value.all.return_value = []
                                
                                # Mock Utils to raise ValueError for empty query
                                mock_utils.validate_non_empty.side_effect = ValueError("Empty query")
                                
                                queries = [{"email": "test@example.com"}]
                                
                                with pytest.raises(TableEmptyError):
                                    StorageService.find_any(mock_session, queries, User)

    @pytest.mark.unit
    @pytest.mark.storage
    def test_update(self):
        """Test update method"""
        mock_session = Mock()
        mock_user = Mock(spec=User)
        mock_user.id = 1
        mock_user.email = "updated@example.com"
        
        with patch('api.storage.storage_service.update') as mock_update_func:
            with patch('api.storage.storage_service.and_') as mock_and:
                with patch('api.storage.storage_service.StorageService.find') as mock_find:
                    # Mock update statement
                    mock_statement = Mock()
                    mock_update_func.return_value = mock_statement
                    mock_statement.where.return_value = mock_statement
                    mock_statement.values.return_value = mock_statement
                    mock_find.return_value = mock_user
                    
                    result = StorageService.update(mock_session, {"id": 1}, {"email": "updated@example.com"}, User)
                    
                    assert result == mock_user
                    mock_session.execute.assert_called_once_with(mock_statement)
                    mock_session.commit.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.storage
    def test_insert(self):
        """Test insert method"""
        mock_session = Mock()
        mock_user = Mock(spec=User)
        mock_user.id = 1
        mock_user.email = "test@example.com"
        
        result = StorageService.insert(mock_session, mock_user)
        
        assert result == mock_user
        mock_session.add.assert_called_once_with(mock_user)
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(mock_user)

    @pytest.mark.unit
    @pytest.mark.storage
    def test_delete(self):
        """Test delete method"""
        mock_session = Mock()
        mock_user = Mock(spec=User)
        mock_user.id = 1
        
        with patch('api.storage.storage_service.select') as mock_select:
            with patch('api.storage.storage_service.and_') as mock_and:
                # Mock select statement
                mock_statement = Mock()
                mock_select.return_value = mock_statement
                mock_statement.where.return_value = mock_statement
                mock_session.execute.return_value.scalars.return_value.all.return_value = [mock_user]
                
                StorageService.delete(mock_session, {"id": 1}, User)
                
                mock_session.delete.assert_called_once_with(mock_user)
                mock_session.commit.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.storage
    def test_get_user_by_google_id(self):
        """Test get_user_by_google_id method"""
        mock_user = Mock(spec=User)
        mock_user.id = 1
        mock_user.google_id = "google123"
        
        with patch('api.storage.storage_service.Session') as mock_session_class:
            with patch('api.storage.storage_service.StorageService.engine') as mock_engine:
                # Mock session and query
                mock_session_instance = Mock()
                mock_session_class.return_value.__enter__.return_value = mock_session_instance
                mock_query = Mock()
                mock_session_instance.query.return_value = mock_query
                mock_query.filter.return_value = mock_query
                mock_query.first.return_value = mock_user
                
                result = StorageService.get_user_by_google_id("google123")
                
                assert result == mock_user
                mock_query.filter.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.storage
    def test_update_user_google_id(self):
        """Test update_user_google_id method"""
        mock_user = Mock(spec=User)
        mock_user.id = 1
        mock_user.google_id = None
        
        with patch('api.storage.storage_service.Session') as mock_session_class:
            with patch('api.storage.storage_service.StorageService.engine') as mock_engine:
                # Mock session and query
                mock_session_instance = Mock()
                mock_session_class.return_value.__enter__.return_value = mock_session_instance
                mock_query = Mock()
                mock_session_instance.query.return_value = mock_query
                mock_query.filter.return_value = mock_query
                mock_query.first.return_value = mock_user
                
                result = StorageService.update_user_google_id(1, "google123")
                
                assert result == mock_user
                assert mock_user.google_id == "google123"
                mock_session_instance.commit.assert_called_once()
                mock_session_instance.refresh.assert_called_once_with(mock_user)

    @pytest.mark.unit
    @pytest.mark.storage
    def test_update_user_google_id_user_not_found(self):
        """Test update_user_google_id method when user not found"""
        with patch('api.storage.storage_service.Session') as mock_session_class:
            with patch('api.storage.storage_service.StorageService.engine') as mock_engine:
                # Mock session and query
                mock_session_instance = Mock()
                mock_session_class.return_value.__enter__.return_value = mock_session_instance
                mock_query = Mock()
                mock_session_instance.query.return_value = mock_query
                mock_query.filter.return_value = mock_query
                mock_query.first.return_value = None
                
                result = StorageService.update_user_google_id(999, "google123")
                
                assert result is None
                mock_session_instance.commit.assert_not_called()

    @pytest.mark.unit
    @pytest.mark.storage
    def test_create_user(self):
        """Test create_user method"""
        with patch('api.storage.storage_service.Session') as mock_session_class:
            with patch('api.storage.storage_service.StorageService.engine') as mock_engine:
                with patch('api.storage.storage_service.User') as mock_user_class:
                    # Mock session and user creation
                    mock_session_instance = Mock()
                    mock_session_class.return_value.__enter__.return_value = mock_session_instance
                    mock_user = Mock(spec=User)
                    mock_user_class.return_value = mock_user
                    
                    result = StorageService.create_user(
                        name="Test User",
                        email="test@example.com",
                        password_hash="hashed_password",
                        google_id="google123",
                        intends_to_be_tutor=True
                    )
                    
                    assert result == mock_user
                    mock_user_class.assert_called_once_with(
                        name="Test User",
                        email="test@example.com",
                        password_hash="hashed_password",
                        google_id="google123",
                        intends_to_be_tutor=True
                    )
                    mock_session_instance.add.assert_called_once_with(mock_user)
                    mock_session_instance.commit.assert_called_once()
                    mock_session_instance.refresh.assert_called_once_with(mock_user)

    @pytest.mark.unit
    @pytest.mark.storage
    def test_get_user_by_email(self):
        """Test get_user_by_email method"""
        mock_user = Mock(spec=User)
        mock_user.id = 1
        mock_user.email = "test@example.com"
        
        with patch('api.storage.storage_service.Session') as mock_session_class:
            with patch('api.storage.storage_service.StorageService.engine') as mock_engine:
                # Mock session and query
                mock_session_instance = Mock()
                mock_session_class.return_value.__enter__.return_value = mock_session_instance
                mock_query = Mock()
                mock_session_instance.query.return_value = mock_query
                mock_query.filter.return_value = mock_query
                mock_query.first.return_value = mock_user
                
                result = StorageService.get_user_by_email("test@example.com")
                
                assert result == mock_user
                mock_query.filter.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.storage
    def test_get_user_by_email_not_found(self):
        """Test get_user_by_email method when user not found"""
        with patch('api.storage.storage_service.Session') as mock_session_class:
            with patch('api.storage.storage_service.StorageService.engine') as mock_engine:
                # Mock session and query
                mock_session_instance = Mock()
                mock_session_class.return_value.__enter__.return_value = mock_session_instance
                mock_query = Mock()
                mock_session_instance.query.return_value = mock_query
                mock_query.filter.return_value = mock_query
                mock_query.first.return_value = None
                
                result = StorageService.get_user_by_email("nonexistent@example.com")
                
                assert result is None
