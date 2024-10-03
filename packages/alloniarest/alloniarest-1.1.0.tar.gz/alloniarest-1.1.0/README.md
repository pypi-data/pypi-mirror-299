# Public Project AllOnIARest

Implements several client objects to access easily AllOnIA's public APIs
(provided you have a valid token of course).

```python
from alloniarest import Client

url = ...
token_id = ...
token_secret = ...

client = Client(
    url,
    user_token={
        "id": token_id, "token": token_secret
    },
    trace=False
)
response = client.request(
    "GET",
    "/some/route?var=value"
)
```