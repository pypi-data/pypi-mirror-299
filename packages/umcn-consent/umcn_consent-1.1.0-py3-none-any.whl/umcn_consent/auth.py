import requests


def authenticate(username, password, client_id, auth_token):
    """
    Initializes an authenticated requests session based on configuration data.

    Returns
    -------
    requests.Session or None
        An authenticated session if the data is correct, or None if required
        configuration data is missing or in case of an error.

    """
    if not username or not password:
        return None

    if not client_id or not auth_token:
        return None

    try:
        session = requests.sessions.Session()
        session.auth = (username, password)
        session.headers.update(
            {
                "Client-ID": client_id,
                "Authorization": auth_token,
            }
        )
        return session
    except requests.RequestException as e:
        print(e)
        return None
