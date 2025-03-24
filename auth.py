import requests
import json
import os
from datetime import datetime, timedelta

def get_beatport_token(username, password, save_to_file=True):
    """
    Get a Beatport API access token using username and password.
    
    Args:
        username (str): Your Beatport username (email)
        password (str): Your Beatport password
        save_to_file (bool): Whether to save the token to a file
        
    Returns:
        dict: Token information including access_token
    """
    url = "https://api.beatport.com/v4/auth/o/token/"
    
    # Using the User Password Grant Flow
    payload = {
        'username': username,
        'password': password,
        'grant_type': 'password'
    }
    
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        
        # Parse response
        token_data = response.json()
        
        # Calculate and add expiration time
        expires_in = token_data.get('expires_in', 3600)
        expires_at = datetime.now() + timedelta(seconds=expires_in)
        token_data['expires_at'] = expires_at.isoformat()
        
        # Save token to file if requested
        if save_to_file:
            with open('.beatport_token.json', 'w') as f:
                json.dump(token_data, f)
            print("Token saved to .beatport_token.json")
        
        return token_data
        
    except Exception as e:
        print(f"Error obtaining access token: {e}")
        if 'response' in locals() and hasattr(response, 'text'):
            print(f"Response: {response.text}")
        return None

def refresh_token(refresh_token_str):
    """
    Refresh an existing token.
    
    Args:
        refresh_token_str (str): The refresh token
        
    Returns:
        dict: New token information
    """
    url = "https://api.beatport.com/v4/auth/o/token/"
    
    payload = {
        'refresh_token': refresh_token_str,
        'grant_type': 'refresh_token'
    }
    
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        
        # Parse response
        token_data = response.json()
        
        # Calculate and add expiration time
        expires_in = token_data.get('expires_in', 3600)
        expires_at = datetime.now() + timedelta(seconds=expires_in)
        token_data['expires_at'] = expires_at.isoformat()
        
        # Save the updated token
        with open('.beatport_token.json', 'w') as f:
            json.dump(token_data, f)
        
        return token_data
        
    except Exception as e:
        print(f"Error refreshing token: {e}")
        if 'response' in locals() and hasattr(response, 'text'):
            print(f"Response: {response.text}")
        return None

def get_current_token():
    """
    Get the current token from file, refreshing if needed.
    
    Returns:
        str: Access token or None if not available
    """
    if not os.path.exists('.beatport_token.json'):
        print("No token file found. Please authenticate first.")
        return None
    
    try:
        with open('.beatport_token.json', 'r') as f:
            token_data = json.load(f)
        
        # Check if token is expired
        expires_at = datetime.fromisoformat(token_data.get('expires_at', '2000-01-01'))
        if expires_at <= datetime.now():
            print("Token expired, refreshing...")
            new_token_data = refresh_token(token_data.get('refresh_token'))
            if new_token_data:
                return new_token_data.get('access_token')
            else:
                return None
        
        return token_data.get('access_token')
        
    except Exception as e:
        print(f"Error loading token: {e}")
        return None

def make_api_request(endpoint, method='GET', params=None, data=None):
    """
    Make an authenticated request to the Beatport API.
    
    Args:
        endpoint (str): API endpoint (without base URL)
        method (str): HTTP method ('GET', 'POST', etc.)
        params (dict): URL parameters
        data (dict): Request body for POST/PUT
            
    Returns:
        dict: Response JSON data or None on error
    """
    token = get_current_token()
    if not token:
        print("No valid token available. Please authenticate first.")
        return None
    
    url = f"https://api.beatport.com/v4/{endpoint.lstrip('/')}"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.request(
            method,
            url,
            headers=headers,
            params=params,
            json=data if method in ['POST', 'PUT', 'PATCH'] else None
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"API request error: {e}")
        if 'response' in locals() and hasattr(response, 'text'):
            print(f"Response: {response.text}")
        return None

if __name__ == "__main__":
    import getpass
    
    # Simple command line interface
    print("Beatport API Token Manager")
    print("--------------------------")
    
    # Check if we already have a valid token
    token = get_current_token()
    if token:
        print(f"Using existing token: {token[:10]}... (truncated)")
        print("Would you like to: ")
        print("1. Test the token")
        print("2. Get a new token")
        choice = input("Enter choice (1 or 2): ")
        
        if choice == '1':
            # Test the token with a simple request
            result = make_api_request('auth/o/introspect/')
            if result:
                print("\nAPI Test Result:")
                print(json.dumps(result, indent=2))
        elif choice == '2':
            # Get new token logic below
            token = None
    
    # If no valid token, get a new one
    if not token:
        print("Using USERNAME and PASSWORD from .env")
        username = os.getenv('BEATPORT_USERNAME')
        password = os.getenv('BEATPORT_PASSWORD')
        
        token_data = get_beatport_token(username, password)
        if token_data:
            print(f"Successfully obtained token: {token_data['access_token'][:10]}... (truncated)")
            
            # Test the token
            test = input("Would you like to test the token? (y/n): ")
            if test.lower() == 'y':
                result = make_api_request('auth/o/introspect/')
                if result:
                    print("\nAPI Test Result:")
                    print(json.dumps(result, indent=2))