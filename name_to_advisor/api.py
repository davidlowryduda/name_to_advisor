"""
api.py -- get advisor using the MathGenealogy APIv2
"""
import requests
import json
from getpass import getpass


PROTOCOL = "https"
HOSTNAME = "mathgenealogy.org"
PORT = "8000"


def get_login():
    """
    Prompt on the console for the user's email and password. Note that the
    password is not shown when the user types it.
    """
    print("Enter email for MathGenealogy authentication:", end=" ")
    email = input()
    password = getpass()
    return {'email': email, 'password': password}


def login(auth):
    """
    Login to the MGP API and get a token for this session. `authdata` should be
    obtained via `get_login()` or equivalent.
    """
    req = requests.post(
        f"{PROTOCOL}://{HOSTNAME}:{PORT}/login",
        auth, timeout=10
    )
    if req.ok:
        print("Token obtained and will expire in 2 hours.")
        req.close()
        return req.json()
    req.close()
    raise RuntimeError("Failed to authenticate")


def do_query(endpoint, jwt_token, query_params):
    """
    Query the MGP API endpoint.

    `jwt_token` should be returned by `login()` or equivalent.

    `query_params` is a dictionary of {KEY: VALUE} pairs for the query.

    EXAMPLE:
      David Lowry-Duda's MGP id is 219943. The following query retrieves
      the rest of the information in MGP.

          do_query('/api/v2/MGP/acad', jwt_token, {'id': 219943})
    """
    headers = {'x-access-token': jwt_token['token']}
    req = requests.get(
        f"{PROTOCOL}://{HOSTNAME}:{PORT}{endpoint}",
        headers=headers,
        params=query_params,
        timeout=15
    )
    if req.ok:
        req.close()
        return req.text
    req.close()
    raise RuntimeError("Error executing query")


def search_for_id(name, jwt_token):
    """
    Query the MGP API to find the MGP ID for 'name'.

    This is naive. We assume that the first space in a name separates the first
    name and the last name. If 0 or 2+ IDs are found, an error is raised and
    these IDs are printed.
    """
    try:
        first, last = name.split(' ', maxsplit=1)
    except:
        raise KeyError(f"No ID found for {name}.")
    endpoint = '/api/v2/MGP/search'
    ids = json.loads(
      do_query(endpoint, jwt_token, {'family_name': last, 'given_name': first})
    )
    if len(ids) == 1:
        return ids[0]
    if len(ids) == 0:
        raise KeyError(f"No ID found for {name}.")
    raise KeyError(f"{name} has multiple possible ids: {ids}")


def advisors_from_name(name, jwt_token):
    """
    Retrieve the advisors for name.

    First, query the MGP API to get the id for name. Then find the advisors.
    """
    try:
        _id = search_for_id(name, jwt_token)
        return advisors_from_id(_id, jwt_token)
    except KeyError:
        print(f"Problem with {name}. Skipping...")
    return []


def advisors_from_id(_id, jwt_token):
    """
    Query the MGP API to find the advisor for the person with given MGP ID.

    The ID can can found from `search_for_id`.
    """
    endpoint = '/api/v2/MGP/acad'
    try:
        data = json.loads(
            do_query(endpoint, jwt_token, {'id': _id})
        )
    except RuntimeError:
        print(f"Error for id {_id}. Skipping this ID.")
        return []
    return advisors_from_json_packet(data)


def advisors_from_json_packet(data):
    """
    Parse MGP json packet for advisors.
    """
    data = data['MGP_academic']['student_data']['degrees']
    advisors = []
    for degree in data:
        for _, advisor in degree['advised by'].items():
            advisors.append(advisor)
    return advisors
