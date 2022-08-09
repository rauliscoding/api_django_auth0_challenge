# API built on top of the [Hello World API](https://github.com/auth0-developer-hub/api_django_python_hello-world/tree/basic-role-based-access-control)

You can use this sample project to retrieve your tenant's applications, as well as the actions that apply to each application and the type of trigger each Action is bound to.

## Get Started

Prerequisites:
    
* Python >= 3.7

Initialize a python virtual environment:

```bash
python3 -m venv venv
source ./venv/bin/activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

Setup virtual environments:
Copy the `.env.example` file to `.env` and edit it to populate its variables.
```bash
cp .env.example .env
```

Run the following command to generate a random secret key and add it to your `.env` file.
```bash
python manage.py generate_secret

# .env
DJANGO_SECRET_KEY=<generated_key>
```

Run DB migrations:

```bash
python manage.py migrate
```

Run the project:

```bash
gunicorn
```

## API Endpoints

The API server defines the following endpoints:



> You need to protect this endpoint using Auth0.

### 🔓 Get applications details

> This endpoint is protected using Auth0 and Role-Based Access Control (RBAC).

```bash
GET /api/applications-details
```

#### Response

```bash
Status: 200 OK
```

```json
{
  "Auth0 Management API (Test Application)": {
    "client_id": "lO7kZ6zsgZDYAkHBY9pl2321",
    "actions": [
      {
        "name": "action_two",
        "status": "deployed",
        "trigger_id": "post-login"
      }
    ]
  },
  "API Explorer Application": {
    "client_id": "eBQasLhcDEToTH1233",
    "actions": [
      {
        "name": "Test Action",
        "status": "deployed",
        "trigger_id": "credentials-exchange"
      },
      {
        "name": "action_two",
        "status": "deployed",
        "trigger_id": "post-login"
      }
    ]
  }
}
```

## Error Handling

### 400s errors

```bash
Status: Corresponding 400 status code
```

```json
{
  "message": "Not Found"
}
```

**Request without authorization header**
```bash
curl localhost:6060/api/applications-details
```
```json
{
  "message":"Authentication credentials were not provided.",
}
```
HTTP Status: `401`

**Request with malformed authorization header**
```bash
curl localhost:6060/api/applications-details --header "authorization: <valid_token>"
```
```json
{
  "message":"Authentication credentials were not provided.",
}
```
HTTP Status: `401`

**Request with wrong authorization scheme**
```bash
curl localhost:6060/api/applications-details --header "authorization: Basic <valid_token>"
```
```json
{
  "message":"Authentication credentials were not provided.",
}
```
HTTP Status: `401`

**Request without token**
```bash
curl localhost:6060/api/applications-details --header "authorization: Bearer"
```
```json
{
  "message":"Authorization header must contain two space-delimited values",
}
```
HTTP Status: `401`

**JWT validation error**
```bash
curl localhost:6060/api/applications-details --header "authorization: Bearer asdf123"
```
```json
{
  "message":"Given token not valid for any token type",
}
```
HTTP Status: `401`

**Token without required permissions**
```bash
curl localhost:6060/api/applications-details --header "authorization: Bearer <token_without_permissions>"
```
```json
{
  "error":"insufficient_permissions",
  "error_description":"You do not have permission to perform this action.",
  "message":"Permission denied"
}
```
HTTP Status: `403`

**Token without the needed scope**
```bash
curl localhost:6060/api/applications-details --header "authorization: Bearer <token_without_read_action_scope>"
```
```json
{
  "status_code": 403,
  "error_description": "insufficient_scope",
  "message": "Insufficient scope, expected any of: read:actions",
  "exception": True,
}
```
### 500s errors


```bash
Status: 500 Internal Server Error
```

```json
{
  "message": "Server Error"
}
```
