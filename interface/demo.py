import requests

def get_organizations(access_token):
    """
    Retrieve organizations from the endpoint using JWT Bearer authentication.
    
    Args:
        access_token (str): The JWT access token.
    
    Returns:
        dict: The JSON response from the endpoint.
    """
    url = 'http://127.0.0.1:8000/api/organisations/'  # Replace with your actual URL
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {
            'status': 'error',
            'message': f'Failed to retrieve organizations, status code: {response.status_code}',
            'data': response.json()
        }

def create_organization(access_token, organization_data):
    """
    Create an organization by posting to the endpoint using JWT Bearer authentication.
    
    Args:
        access_token (str): The JWT access token.
        organization_data (dict): The data for the new organization.
    
    Returns:
        dict: The JSON response from the endpoint.
    """
    url = 'http://127.0.0.1:8000/api/organisations/'  # Replace with your actual URL
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(url, json=organization_data, headers=headers)
    
    if response.status_code == 201:
        return response.json()
    else:
        return {
            'status': 'error',
            'message': f'Failed to create organization, status code: {response.status_code}',
            'data': response.json()
        }
    
import requests

def add_user_to_organization(access_token, org_id, user_id):
    """
    Adds a user to an organization using JWT Bearer authentication.
    
    Args:
        access_token (str): The JWT access token.
        org_id (str): The organization ID.
        user_id (str): The user ID to be added.
    
    Returns:
        dict: The JSON response from the endpoint.
    """
    url = f'http://127.0.0.1:8000/api/organisations/{org_id}/users'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'userId': user_id
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {
            'status': 'error',
            'message': f'Failed to add user to organization, status code: {response.status_code}',
            'data': response.json()
        }

# Example usage:
access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIwNzE5OTY3LCJpYXQiOjE3MjA3MTk2NjcsImp0aSI6IjIzY2FlNThmYzBiZjRiMjBhNjE5Y2U5YTFiZDc5MDdkIiwidXNlcl9pZCI6ImZhZWJlNDY0LTllMWItNGE5NC04NDI3LThiNWQ0Y2I2YzIzYyJ9.2dy8eP4FJViWL5Rv2mKzaeIWjn0J16YH8Tx4QQCwzQU'
org_id = '07dce907-b7d1-4293-8045-ace33df1ff59'
user_id = 'faebe464-9e1b-4a94-8427-8b5d4cb6c23c'

response = add_user_to_organization(access_token, org_id, user_id)
print(response)


# Example usage:
access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIwNjkzMzMzLCJpYXQiOjE3MjA2OTMwMzMsImp0aSI6IjllNDk5NzkzYjk5ZTRjNTFhOGQ3ZTc4Yzk0NGVlNzM5IiwidXNlcl9pZCI6IjAwZGFmZTI2LTQxNDEtNDVhYy1hNThiLTJlNWYxMWFjZGI4NiJ9.OweOhAUfRADZxwkHyAzXQecWVZ_N1cTSZXd5AOnFNuQ'
organization_data = {
    'name': 'New Organization',
    'description': 'My description'
}

# Retrieve organizations
org_response = get_organizations(access_token)
print(org_response)

# Create a new organization
create_response = create_organization(access_token, organization_data)
print(create_response)
