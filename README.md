# Grinning Cat Python SDK

----

**Grinning Cat Python SDK** is a library to help the implementation
of [Grinning Cat](https://github.com/matteocacciola/grinning-cat-core) on a Python Project

* [Installation](#installation)
* [Usage](#usage)

## Installation

To install Grinning Cat Python SDK, run:

```bash
pip install grinning-cat-python-sdk
```

## Usage
Initialization and usage:

```python
from grinning_cat_python_sdk import GrinningCatClient, Configuration

configuration = Configuration(host="localhost", port=1865, auth_key="test", secure_connection=False)

cat_client = GrinningCatClient(configuration)
```

Authenticate with a username and password (the client keeps the returned access token for the following calls),
refresh it before it expires, and log out to revoke the session:

```python
from grinning_cat_python_sdk import GrinningCatClient, Configuration

configuration = Configuration(host="localhost", port=1865, auth_key="test", secure_connection=False)
cat_client = GrinningCatClient(configuration)

token = cat_client.auth.token("username", "password")
# token.access_token, token.expires_in, token.refresh_token, token.refresh_expires_in

# before the access token expires, exchange the (single-use) refresh token for a new pair
token = cat_client.auth.refresh(token.refresh_token)

# revoke the session; already-issued access tokens stay valid until they expire
cat_client.auth.logout(token.refresh_token)
```
Send a message to the websocket:

```python
from grinning_cat_python_sdk import GrinningCatClient, Configuration, Message

configuration = Configuration(host="localhost", port=1865, auth_key="test", secure_connection=False)
cat_client = GrinningCatClient(configuration)

notification_closure = lambda message: None # handle websocket notification, like chat token stream

# result is the result of the message
result = cat_client.message.send_websocket_message(
    Message(text="Hello world!"),  # message body
    "agent", # agent ID
    "user", # user ID
    callback=notification_closure # websocket notification closure handle
)
```

Load data to the rabbit hole:
```python
import asyncio

from grinning_cat_python_sdk import GrinningCatClient, Configuration, Message

configuration = Configuration(host="localhost", port=1865, auth_key="test", secure_connection=False)
cat_client = GrinningCatClient(configuration)

# file
file = "path/to/file"
result = asyncio.run(cat_client.rabbit_hole.post_file(file, "agent"))

# url
url = "https://www.google.com"
result = asyncio.run(cat_client.rabbit_hole.post_web(url, "agent"))
```

Memory management utilities:

```python
from grinning_cat_python_sdk import GrinningCatClient, Configuration, Message

configuration = Configuration(host="localhost", port=1865, auth_key="test", secure_connection=False)
cat_client = GrinningCatClient(configuration)

cat_client.memory.get_memory_collections("agent")  # get number of vectors in the working memory
cat_client.memory.get_memory_recall("HELLO", "agent", "user")  # recall memories by text

url = "https://www.google.com"

# delete memory points by metadata, like this example delete by source
cat_client.memory.delete_memory_points_by_metadata("declarative", "agent", {"source": url})
```
