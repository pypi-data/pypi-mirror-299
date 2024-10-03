import os
from dotenv import load_dotenv
import requests
from .exceptions import AuthenticationError, APIError

class APIClient:
    def __init__(self, env_file='.env', test_env=None):
        if test_env is None:
            load_dotenv(env_file)
            self.host = os.getenv('API_HOST')
            self.api_key = os.getenv('API_KEY')
        else:
            self.host = test_env.get('API_HOST')
            self.api_key = test_env.get('API_KEY')

        if not self.host or not self.api_key:
            raise ValueError("API_HOST and API_KEY must be set in the .env file or as environment variables")

        self.session = requests.Session()
        self._auth_token = None

    def authenticate(self):
        url = f"{self.host}/api/v1/authenticate"
        headers = {'X-API-Key': self.api_key}

        response = self.session.get(url, headers=headers)

        if response.status_code != 200:
            raise AuthenticationError(f"Authentication failed: {response.text}")

        data = response.json()
        self._auth_token = data.get('authToken')
        if not self._auth_token:
            raise AuthenticationError("No session token received from authentication endpoint")
        return self._auth_token

    @property
    def auth_token(self):
        if not self._auth_token:
            self.authenticate()
        return self._auth_token

    def call_api(self, method, endpoint, **kwargs):
        headers = kwargs.pop('headers', {})
        headers['X-API-Key'] = self.api_key
        headers['X-Auth-Token'] = self.auth_token

        url = f"{self.host}{endpoint}"
        response = self.session.request(method, url, headers=headers, **kwargs)

        if response.status_code == 401:  # Unauthorized, token might have expired
            self._auth_token = None  # Clear the token
            self.authenticate()  # Re-authenticate
            headers['X-Auth-Token'] = self.auth_token  # Update the token in headers
            response = self.session.request(method, url, headers=headers, **kwargs)  # Retry the request

        if response.status_code != 200:
            raise APIError(f"API call failed: {response.text}")

        return response.json()

    def get_applied_filters(self):
        """
        Fetch the applied filters from the API.

        Returns:
            dict: A dictionary containing the applied filters and other response data.

        Raises:
            APIError: If the API call fails.
        """
        return self.call_api('GET', '/api/v1/filters')

    def get_models(self):
        """
        Fetch all models from the API.

        Returns:
            dict: A dictionary containing the models and other response data.

        Raises:
            APIError: If the API call fails.
        """
        return self.call_api('GET', '/api/v1/models')

    def create_model(self, model_data):
        """
        Create a new model.

        Args:
            model_data (dict): A dictionary containing the model details.
                Required keys: url, model, label, vendor, token
                Optional key: image

        Returns:
            dict: A dictionary containing the created model's ID and other response data.

        Raises:
            ValueError: If required parameters are missing or invalid.
            APIError: If the API call fails.
        """
        required_fields = ['url', 'model', 'label', 'vendor', 'token']
        for field in required_fields:
            if field not in model_data:
                raise ValueError(f"Missing required field: {field}")

        return self.call_api('POST', '/api/v1/models', json=model_data)

    def create_session(self, session_name):
        """
        Create a new chat session.

        Args:
            session_name (str): The name of the session to create.

        Returns:
            dict: A dictionary containing the session ID and other response data.

        Raises:
            APIError: If the API call fails.
        """
        data = {"sessionName": session_name}
        return self.call_api('POST', '/api/v1/session/create', json=data)

    def delete_session(self, session_id):
        """
        Delete a chat session.

        Args:
            session_id (str): The ID of the session to delete.

        Returns:
            dict: A dictionary containing response data.

        Raises:
            APIError: If the API call fails.
            ValueError: If session_id is invalid.
        """
        if not isinstance(session_id, str) or not session_id:
            raise ValueError("session_id must be a non-empty string")
        data = {"sessionId": session_id}
        return self.call_api('POST', '/api/v1/session/delete', json=data)

    def rename_session(self, session_id, new_name):
        """
        Rename a chat session.

        Args:
            session_id (str): The ID of the session to rename.
            new_name (str): The new name for the session.

        Returns:
            dict: A dictionary containing response data.

        Raises:
            APIError: If the API call fails or if a session with the new name already exists.
            ValueError: If session_id or new_name is invalid.
        """
        if not session_id or not isinstance(session_id, str):
            raise ValueError("session_id must be a non-empty string")
        if not new_name or not isinstance(new_name, str):
            raise ValueError("new_name must be a non-empty string")

        data = {"sessionId": session_id, "newName": new_name}
        return self.call_api('POST', '/api/v1/session/rename', json=data)

    def check_token_usage(self):
        """
        Check the token usage for the current user.

        Returns:
            dict: A dictionary containing token usage information.

        Raises:
            APIError: If the API call fails.
        """
        return self.call_api('GET', '/api/v1/tokens')

    def filter_text(self, text, session_id):
        """
        Filter the given text using applicable filters.

        Args:
            text (str): The text to be filtered.
            session_id (str): The ID of the session associated with this text.

        Returns:
            dict: A dictionary containing the filtered text, filter counts, hash map, and message ID.

        Raises:
            APIError: If the API call fails.
            ValueError: If text or session_id is invalid.
        """
        if not text or not isinstance(text, str):
            raise ValueError("text must be a non-empty string")
        if not isinstance(session_id, str) or not session_id:
            raise ValueError("session_id must be a non-empty string")

        data = {"text": text, "sessionId": session_id}
        return self.call_api('POST', '/api/v1/filterText', json=data)

    def submit_message(self, model, prompt, filter_data):
        """
        Submit a message to the LLM model.

        Args:
            model (dict): A dictionary containing model details.
            prompt (dict): A dictionary containing prompt details.
            filter_data (dict): A dictionary containing filter data.

        Returns:
            dict: The response from the LLM model.

        Raises:
            ValueError: If required parameters are missing or invalid.
            APIError: If the API call fails.
            AuthenticationError: If authentication fails.
        """
        if not isinstance(model, dict) or not isinstance(prompt, dict) or not isinstance(filter_data, dict):
            raise ValueError("model, prompt, and filter_data must be dictionaries")

        data = {
            "model": model,
            "prompt": prompt,
            "filter": filter_data
        }

        return self.call_api('POST', '/api/v1/message', json=data)

    def get_session_messages(self, session_id):
        """
        Retrieve messages for a specific chat session.

        Args:
            session_id (str): The ID of the session to retrieve messages from.

        Returns:
            dict: A dictionary containing the session messages and other response data.

        Raises:
            APIError: If the API call fails.
            ValueError: If session_id is invalid.
        """
        if not isinstance(session_id, str) or not session_id:
            raise ValueError("session_id must be a non-empty string")

        data = {"sessionId": session_id}
        return self.call_api('GET', '/api/v1/session/messages', json=data)

    def get_sessions(self, start_time=None, end_time=None):
        """
        Retrieve sessions within a specified time range.

        Args:
            start_time (str, optional): The start time for the session range (ISO 8601 format).
            end_time (str, optional): The end time for the session range (ISO 8601 format).

        Returns:
            dict: A dictionary containing the sessions and other response data.

        Raises:
            APIError: If the API call fails.
        """
        params = {}
        if start_time:
            params['startTime'] = start_time
        if end_time:
            params['endTime'] = end_time

        return self.call_api('GET', '/api/v1/session', params=params)

    def login(self, email, password):
        """
        Login with email and password.

        Args:
            email (str): The user's email.
            password (str): The user's password.

        Returns:
            dict: A dictionary containing the user ID and auth token.

        Raises:
            APIError: If the API call fails.
            ValueError: If email or password is invalid.
        """
        if not email or not isinstance(email, str):
            raise ValueError("email must be a non-empty string")
        if not password or not isinstance(password, str):
            raise ValueError("password must be a non-empty string")

        data = {"email": email, "password": password}
        return self.call_api('POST', '/api/v1/login', json=data)

    def login_with_google(self, access_token):
        """
        Login with Google SSO.

        Args:
            access_token (str): The Google access token.

        Returns:
            dict: A dictionary containing the user ID and auth token.

        Raises:
            APIError: If the API call fails.
            ValueError: If access_token is invalid.
        """
        if not access_token or not isinstance(access_token, str):
            raise ValueError("access_token must be a non-empty string")

        data = {"accessToken": access_token}
        return self.call_api('POST', '/api/v1/login/google', json=data)

    def register(self, email, password, profile=None):
        """
        Register a new user.

        Args:
            email (str): The user's email.
            password (str): The user's password.
            profile (dict, optional): Additional profile information.

        Returns:
            dict: A dictionary containing the user ID and auth token.

        Raises:
            APIError: If the API call fails.
            ValueError: If email or password is invalid.
        """
        if not email or not isinstance(email, str):
            raise ValueError("email must be a non-empty string")
        if not password or not isinstance(password, str):
            raise ValueError("password must be a non-empty string")

        data = {"email": email, "password": password}
        if profile:
            if not isinstance(profile, dict):
                raise ValueError("profile must be a dictionary")
            data["profile"] = profile

        return self.call_api('POST', '/api/v1/register', json=data)

    def logout(self):
        """
        Logout the current user.

        Returns:
            dict: A dictionary containing the response message.

        Raises:
            APIError: If the API call fails.
        """
        return self.call_api('POST', '/api/v1/logout')
