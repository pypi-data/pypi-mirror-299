import pytest
from unittest.mock import patch, Mock
from strongly import APIClient
from strongly.exceptions import AuthenticationError, APIError

def test_init_missing_env(monkeypatch):
    monkeypatch.delenv('API_HOST', raising=False)
    monkeypatch.delenv('API_KEY', raising=False)
    with pytest.raises(ValueError):
        APIClient(test_env={})  # Pass an empty dict as test_env

def test_authenticate_success(api_client):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'authToken': 'test-auth-token'}
    api_client.session.get.return_value = mock_response

    token = api_client.authenticate()

    assert token == 'test-auth-token'
    assert api_client._auth_token == 'test-auth-token'
    api_client.session.get.assert_called_once_with(
        f"{api_client.host}/api/v1/authenticate",
        headers={'X-API-Key': api_client.api_key}
    )

def test_authenticate_failure(api_client):
    mock_response = Mock()
    mock_response.status_code = 401
    mock_response.text = 'Authentication failed'
    api_client.session.get.return_value = mock_response

    with pytest.raises(AuthenticationError):
        api_client.authenticate()

def test_call_api_success(api_client):
    api_client.authenticate = Mock(return_value='test-auth-token')
    api_client._auth_token = 'test-auth-token'
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'data': 'test-data'}
    api_client.session.request.return_value = mock_response

    result = api_client.call_api('GET', '/test-endpoint')

    assert result == {'data': 'test-data'}
    api_client.session.request.assert_called_once_with(
        'GET',
        'https://api.example.com/test-endpoint',
        headers={'X-API-Key': 'test-api-key', 'X-Auth-Token': 'test-auth-token'}
    )

def test_call_api_token_expired(api_client):
    api_client._auth_token = 'expired-token'
    mock_responses = [
        Mock(status_code=401, text='Unauthorized'),
        Mock(status_code=200, json=Mock(return_value={'data': 'test-data'}))
    ]
    api_client.session.request.side_effect = mock_responses
    api_client.authenticate = Mock(return_value='new-auth-token')

    result = api_client.call_api('GET', '/test-endpoint')

    assert result == {'data': 'test-data'}
    assert api_client.authenticate.called
    assert api_client.session.request.call_count == 2

def test_call_api_failure(api_client):
    api_client.authenticate = Mock(return_value='test-auth-token')
    api_client._auth_token = 'test-auth-token'
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.text = 'Internal Server Error'
    api_client.session.request.return_value = mock_response

    with pytest.raises(APIError):
        api_client.call_api('GET', '/test-endpoint')

def test_get_models(api_client):
    api_client.call_api = Mock(return_value={
        'message': 'Models retrieved successfully',
        'userId': 'test-user-id',
        'models': [
            {'id': '1', 'name': 'Model 1'},
            {'id': '2', 'name': 'Model 2'}
        ]
    })

    result = api_client.get_models()

    assert 'models' in result
    assert len(result['models']) == 2
    assert result['models'][0]['name'] == 'Model 1'
    assert result['userId'] == 'test-user-id'
    api_client.call_api.assert_called_once_with('GET', '/api/v1/models')

def test_get_applied_filters(api_client):
    api_client.call_api = Mock(return_value={
        'message': 'Applied filters retrieved successfully',
        'userId': 'test-user-id',
        'filters': [
            {
                "_id": "11",
                "name": "Address",
                "description": "A street address."
            },
            {
                "_id": "iYafk8FLdus5SGJy2",
                "name": "Food",
                "description": "This is a test of the topic filter to detect food related posts."
            }
        ]
    })

    result = api_client.get_applied_filters()

    assert 'filters' in result
    assert len(result['filters']) == 2
    assert result['filters'][0]['name'] == 'Address'
    assert result['filters'][1]['name'] == 'Food'
    assert result['userId'] == 'test-user-id'
    api_client.call_api.assert_called_once_with('GET', '/api/v1/filters')

def test_create_session(api_client):
    api_client.call_api = Mock(return_value={
        'message': 'Session created successfully',
        'sessionId': 'test-session-id'
    })

    result = api_client.create_session('Test Session')

    assert result['message'] == 'Session created successfully'
    assert result['sessionId'] == 'test-session-id'
    api_client.call_api.assert_called_once_with(
        'POST',
        '/api/v1/session/create',
        json={'sessionName': 'Test Session'}
    )

def test_delete_session(api_client):
    api_client.call_api = Mock(return_value={
        'message': 'Session deleted successfully'
    })

    session_id = 'test-session-id'
    result = api_client.delete_session(session_id)

    assert result['message'] == 'Session deleted successfully'
    api_client.call_api.assert_called_once_with(
        'POST',
        '/api/v1/session/delete',
        json={'sessionId': session_id}
    )

def test_delete_session_invalid_id(api_client):
    invalid_ids = [None, "", 123, []]

    for invalid_id in invalid_ids:
        with pytest.raises(ValueError):
            api_client.delete_session(invalid_id)

def test_rename_session(api_client):
    api_client.call_api = Mock(return_value={
        'message': 'Session renamed successfully'
    })

    session_id = 'test-session-id'
    new_name = 'New Test Session Name'
    result = api_client.rename_session(session_id, new_name)

    assert result['message'] == 'Session renamed successfully'
    api_client.call_api.assert_called_once_with(
        'POST',
        '/api/v1/session/rename',
        json={'sessionId': session_id, 'newName': new_name}
    )

def test_rename_session_invalid_input(api_client):
    invalid_inputs = [
        (None, 'New Name'),
        ('', 'New Name'),
        ('session-id', None),
        ('session-id', ''),
        (123, 'New Name'),
        ('session-id', 123),
    ]

    for session_id, new_name in invalid_inputs:
        with pytest.raises(ValueError):
            api_client.rename_session(session_id, new_name)

def test_check_token_usage(api_client):
    mock_response = {
        'isOverLimit': False,
        'isRestricted': False,
        'userTokenUsage': 5000,
        'planTokenLimit': 10000,
        'companyTokensAvailable': 5000,
        'purchasedTokens': 2000,
    }
    api_client.call_api = Mock(return_value=mock_response)

    result = api_client.check_token_usage()

    assert result == mock_response
    api_client.call_api.assert_called_once_with('GET', '/api/v1/tokens')

def test_filter_text(api_client):
    mock_response = {
        'filteredText': 'This is a [1:sensitive] message.',
        'promptText': 'This is a [1:sensitive] message.',
        'filter': {
            'filterCounts': {'1': 1},
            'alerts': [],
            'alertReasons': [],
            'blocked': [],
            'blockedReasons': [],
            'hashed': ['[1:sensitive]'],
            'isBlocked': False
        },
        'messageId': 'msg123'
    }
    api_client.call_api = Mock(return_value=mock_response)

    result = api_client.filter_text("This is a confidential message.", "session123")

    assert result == mock_response
    api_client.call_api.assert_called_once_with(
        'POST',
        '/api/v1/filterText',
        json={'text': "This is a confidential message.", 'sessionId': "session123"}
    )

def test_filter_text_invalid_input(api_client):
    invalid_inputs = [
        (None, "session123"),
        ("", "session123"),
        (123, "session123"),
        ([], "session123"),
        ("Valid text", None),
        ("Valid text", ""),
        ("Valid text", 123),
        ("Valid text", [])
    ]

    for text, session_id in invalid_inputs:
        with pytest.raises(ValueError):
            api_client.filter_text(text, session_id)

def test_submit_message(api_client):
    mock_response = {
        'content': 'This is a response from the LLM model.'
    }
    api_client.call_api = Mock(return_value=mock_response)

    model = {
        'model': 'gpt-3.5-turbo',
        'modelLabel': 'GPT-3.5 Turbo',
        'messageId': 'msg123',
        'session': {'sessionId': 'session123', 'sessionName': 'Test Session'},
        'temperature': 0.7,
        'max_tokens': 1024
    }
    prompt = {
        'system': 'You are a helpful assistant.',
        'assistant': '',
        'contextPrompts': [],
        'message': 'What is the capital of France?'
    }
    filter_data = {
        'prompt': {
            'filterCounts': {},
            'alerts': [],
            'alertReasons': [],
            'blocked': [],
            'blockedReasons': [],
            'hashed': [],
            'isBlocked': False
        },
        'response': {
            'filterCounts': {},
            'alerts': [],
            'alertReasons': [],
            'blocked': [],
            'blockedReasons': [],
            'hashed': [],
            'isBlocked': False
        }
    }

    result = api_client.submit_message(model, prompt, filter_data)

    assert result == mock_response
    api_client.call_api.assert_called_once_with(
        'POST',
        '/api/v1/message',
        json={
            'model': model,
            'prompt': prompt,
            'filter': filter_data
        }
    )

@patch('strongly.api_client.APIClient.authenticate')
@patch('strongly.api_client.APIClient.call_api')
def test_submit_message_invalid_input(mock_call_api, mock_authenticate, api_client):
    # Set up mocks
    mock_authenticate.return_value = 'mocked_auth_token'
    mock_call_api.return_value = {}

    invalid_inputs = [
        ([], {}, {}),
        ({}, [], {}),
        ({}, {}, []),
        ("string", {}, {}),
        ({}, "string", {}),
        ({}, {}, "string"),
    ]

    for model, prompt, filter_data in invalid_inputs:
        with pytest.raises(ValueError):
            api_client.submit_message(model, prompt, filter_data)

    # Test that valid input (all dictionaries) doesn't raise an exception
    try:
        api_client.submit_message({}, {}, {})
    except ValueError:
        pytest.fail("submit_message raised ValueError unexpectedly with valid input")

    # Verify that call_api was called with the correct arguments
    mock_call_api.assert_called_once_with('POST', '/api/v1/message', json={
        "model": {},
        "prompt": {},
        "filter": {}
    })

    # Test error handling
    mock_call_api.side_effect = APIError("API call failed")
    with pytest.raises(APIError):
        api_client.submit_message({}, {}, {})

    # Reset mock and test authentication error
    mock_call_api.reset_mock()
    mock_call_api.side_effect = AuthenticationError("Authentication failed")
    with pytest.raises(AuthenticationError):
        api_client.submit_message({}, {}, {})

def test_get_session_messages(api_client):
    mock_response = {
        'messages': [
            {'id': 'msg1', 'content': 'Hello', 'role': 'user'},
            {'id': 'msg2', 'content': 'Hi there!', 'role': 'assistant'}
        ]
    }
    api_client.call_api = Mock(return_value=mock_response)

    session_id = 'test-session-id'
    result = api_client.get_session_messages(session_id)

    assert result == mock_response
    api_client.call_api.assert_called_once_with('GET', '/api/v1/session/messages', json={'sessionId': session_id})

def test_get_session_messages_invalid_id(api_client):
    invalid_ids = [None, "", 123, []]

    for invalid_id in invalid_ids:
        with pytest.raises(ValueError):
            api_client.get_session_messages(invalid_id)

def test_get_sessions(api_client):
    mock_response = {
        'message': 'Sessions retrieved successfully',
        'sessions': [
            {'id': 'session1', 'name': 'Session 1'},
            {'id': 'session2', 'name': 'Session 2'}
        ],
        'isAdmin': False
    }
    api_client.call_api = Mock(return_value=mock_response)

    result = api_client.get_sessions('2023-01-01T00:00:00Z', '2023-12-31T23:59:59Z')

    assert result == mock_response
    api_client.call_api.assert_called_once_with(
        'GET',
        '/api/v1/session',
        params={'startTime': '2023-01-01T00:00:00Z', 'endTime': '2023-12-31T23:59:59Z'}
    )

def test_login(api_client):
    mock_response = {
        'userId': 'user123',
        'authToken': 'auth-token-123'
    }
    api_client.call_api = Mock(return_value=mock_response)

    result = api_client.login('user@example.com', 'password123')

    assert result == mock_response
    api_client.call_api.assert_called_once_with(
        'POST',
        '/api/v1/login',
        json={'email': 'user@example.com', 'password': 'password123'}
    )

def test_login_invalid_input(api_client):
    invalid_inputs = [
        (None, 'password'),
        ('', 'password'),
        ('user@example.com', None),
        ('user@example.com', ''),
        (123, 'password'),
        ('user@example.com', 123),
    ]

    for email, password in invalid_inputs:
        with pytest.raises(ValueError):
            api_client.login(email, password)

def test_login_with_google(api_client):
    mock_response = {
        'userId': 'user123',
        'authToken': 'auth-token-123'
    }
    api_client.call_api = Mock(return_value=mock_response)

    result = api_client.login_with_google('google-access-token')

    assert result == mock_response
    api_client.call_api.assert_called_once_with(
        'POST',
        '/api/v1/login/google',
        json={'accessToken': 'google-access-token'}
    )

def test_login_with_google_invalid_input(api_client):
    invalid_inputs = [None, "", 123, []]

    for invalid_token in invalid_inputs:
        with pytest.raises(ValueError):
            api_client.login_with_google(invalid_token)

def test_register(api_client):
    mock_response = {
        'userId': 'user123',
        'authToken': 'auth-token-123'
    }
    api_client.call_api = Mock(return_value=mock_response)

    result = api_client.register('user@example.com', 'password123', {'name': 'Test User'})

    assert result == mock_response
    api_client.call_api.assert_called_once_with(
        'POST',
        '/api/v1/register',
        json={'email': 'user@example.com', 'password': 'password123', 'profile': {'name': 'Test User'}}
    )

def test_register_invalid_input(api_client):
    invalid_inputs = [
        (None, 'password', {}),
        ('', 'password', {}),
        ('user@example.com', None, {}),
        ('user@example.com', '', {}),
        (123, 'password', {}),
        ('user@example.com', 123, {}),
        ('user@example.com', 'password', 'invalid_profile'),
    ]

    for email, password, profile in invalid_inputs:
        with pytest.raises(ValueError):
            api_client.register(email, password, profile)

def test_register_without_profile(api_client):
    mock_response = {
        'userId': 'user123',
        'authToken': 'auth-token-123'
    }
    api_client.call_api = Mock(return_value=mock_response)

    result = api_client.register('user@example.com', 'password123')

    assert result == mock_response
    api_client.call_api.assert_called_once_with(
        'POST',
        '/api/v1/register',
        json={'email': 'user@example.com', 'password': 'password123'}
    )

def test_logout(api_client):
    mock_response = {
        'message': 'Logged out successfully'
    }
    api_client.call_api = Mock(return_value=mock_response)

    result = api_client.logout()

    assert result == mock_response
    api_client.call_api.assert_called_once_with('POST', '/api/v1/logout')

# Additional tests for error handling and edge cases

def test_api_error_handling(api_client):
    api_client.call_api = Mock(side_effect=APIError("API call failed"))

    with pytest.raises(APIError):
        api_client.get_models()

def test_authentication_error_handling(api_client):
    api_client.authenticate = Mock(side_effect=AuthenticationError("Authentication failed"))

    with pytest.raises(AuthenticationError):
        api_client.get_models()

def test_get_sessions_without_time_range(api_client):
    mock_response = {
        'message': 'Sessions retrieved successfully',
        'sessions': [
            {'id': 'session1', 'name': 'Session 1'},
            {'id': 'session2', 'name': 'Session 2'}
        ],
        'isAdmin': False
    }
    api_client.call_api = Mock(return_value=mock_response)

    result = api_client.get_sessions()

    assert result == mock_response
    api_client.call_api.assert_called_once_with('GET', '/api/v1/session', params={})

def test_submit_message_with_minimal_input(api_client):
    mock_response = {
        'content': 'This is a response from the LLM model.'
    }
    api_client.call_api = Mock(return_value=mock_response)

    model = {'model': 'gpt-3.5-turbo'}
    prompt = {'message': 'Hello, world!'}
    filter_data = {}

    result = api_client.submit_message(model, prompt, filter_data)

    assert result == mock_response
    api_client.call_api.assert_called_once_with(
        'POST',
        '/api/v1/message',
        json={
            'model': model,
            'prompt': prompt,
            'filter': filter_data
        }
    )

def test_filter_text_with_long_text(api_client):
    long_text = "This is a very long text. " * 100
    mock_response = {
        'filteredText': long_text,
        'promptText': long_text,
        'filter': {
            'filterCounts': {},
            'alerts': [],
            'alertReasons': [],
            'blocked': [],
            'blockedReasons': [],
            'hashed': [],
            'isBlocked': False
        },
        'messageId': 'msg123'
    }
    api_client.call_api = Mock(return_value=mock_response)

    result = api_client.filter_text(long_text, "session123")

    assert result == mock_response
    api_client.call_api.assert_called_once_with(
        'POST',
        '/api/v1/filterText',
        json={'text': long_text, 'sessionId': "session123"}
    )

def test_get_models_empty_response(api_client):
    api_client.call_api = Mock(return_value={
        'message': 'No models found',
        'userId': 'test-user-id',
        'models': []
    })

    result = api_client.get_models()

    assert 'models' in result
    assert len(result['models']) == 0
    assert result['userId'] == 'test-user-id'
    api_client.call_api.assert_called_once_with('GET', '/api/v1/models')

def test_rename_session_to_existing_name(api_client):
    api_client.call_api = Mock(side_effect=APIError("A session with this name already exists"))

    with pytest.raises(APIError, match="A session with this name already exists"):
        api_client.rename_session('session-id', 'Existing Session Name')

def test_check_token_usage_over_limit(api_client):
    mock_response = {
        'isOverLimit': True,
        'isRestricted': False,
        'userTokenUsage': 15000,
        'planTokenLimit': 10000,
        'companyTokensAvailable': 0,
        'purchasedTokens': 5000,
    }
    api_client.call_api = Mock(return_value=mock_response)

    result = api_client.check_token_usage()

    assert result == mock_response
    assert result['isOverLimit']
    api_client.call_api.assert_called_once_with('GET', '/api/v1/tokens')

def test_login_inactive_user(api_client):
    mock_response = {
        'error': 'Account is inactive. Please contact support.'
    }
    api_client.call_api = Mock(return_value=mock_response, side_effect=APIError("Account is inactive"))

    with pytest.raises(APIError, match="Account is inactive"):
        api_client.login('inactive@example.com', 'password123')

def test_register_existing_user(api_client):
    mock_response = {
        'error': 'Email already exists'
    }
    api_client.call_api = Mock(return_value=mock_response, side_effect=APIError("Email already exists"))

    with pytest.raises(APIError, match="Email already exists"):
        api_client.register('existing@example.com', 'password123')

def test_get_session_messages_empty_session(api_client):
    mock_response = {
        'messages': []
    }
    api_client.call_api = Mock(return_value=mock_response)

    session_id = 'empty-session-id'
    result = api_client.get_session_messages(session_id)

    assert result == mock_response
    assert len(result['messages']) == 0
    api_client.call_api.assert_called_once_with('GET', '/api/v1/session/messages', json={'sessionId': session_id})

def test_submit_message_with_topic_match_error(api_client):
    error_response = {
        'error': 'topic-match',
        'message': 'The message contains restricted topics',
        'details': ['Topic1', 'Topic2']
    }
    api_client.call_api = Mock(side_effect=APIError("The message contains restricted topics"))

    model = {'model': 'gpt-3.5-turbo'}
    prompt = {'message': 'This message contains restricted topics'}
    filter_data = {}

    with pytest.raises(APIError, match="The message contains restricted topics"):
        api_client.submit_message(model, prompt, filter_data)

@patch('strongly.api_client.APIClient.call_api')
def test_create_model(mock_call_api):
    # Arrange
    api_client = APIClient(test_env={
        "API_HOST": "http://localhost:3000",
        "API_KEY": "test_api_key"
    })
    mock_call_api.return_value = {"modelId": "test_model_id"}

    model_data = {
        "url": "https://api.example.com/v1/models/test-model",
        "model": "test-model",
        "label": "Test Model",
        "vendor": "TestVendor",
        "image": "https://example.com/test-model-image.png",
        "token": "test_token"
    }

    # Act
    result = api_client.create_model(model_data)

    # Assert
    assert result == {"modelId": "test_model_id"}
    mock_call_api.assert_called_once_with('POST', '/api/v1/models', json=model_data)

    # Test missing required field
    with pytest.raises(ValueError):
        api_client.create_model({"url": "https://api.example.com/v1/models/test-model"})

    # Test API error
    mock_call_api.side_effect = APIError("API call failed")
    with pytest.raises(APIError):
        api_client.create_model(model_data)
