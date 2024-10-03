# FluidStack Python Library

[![pypi](https://img.shields.io/pypi/v/fluidstack.svg)](https://pypi.python.org/pypi/fluidstack)
[![fern shield](https://img.shields.io/badge/%F0%9F%8C%BF-SDK%20generated%20by%20Fern-brightgreen)](https://github.com/fern-api/fern)

The FluidStack Python Library provides convenient access to the FluidStack API from
applications written in Python.

The library includes type definitions for all
request and response fields, and offers both synchronous and asynchronous clients powered by httpx.

## Installation

Add this dependency to your project's build file:

```bash
pip install fluidstack
# or
poetry add fluidstack
```

## Usage

Simply import `FluidStack` and start making calls to our API.

```python
from fluidstack.client import FluidStack

client = FluidStack(
    api_key="YOUR_API_KEY", # defaults to FLUIDSTACK_API_KEY
)

client.ssh_keys.create(
    name="name",
    public_key="PUBLIC_KEY",
)
```

## Async Client

The SDK also exports an async client so that you can make non-blocking
calls to our API.

```python
from fluidstack.client import AsyncFluidStack

client = AsyncFluidStack(
    api_key="YOUR_API_KEY",
)

async def main() -> None:
    await client.ssh_keys.create(
        name="name",
        public_key="PUBLIC_KEY",
    )
asyncio.run(main())
```

## Exception Handling

All errors thrown by the SDK will be subclasses of [`ApiError`](./src/schematic/core/api_error.py).

```python
import fluidstack

try:
    client.auth.get_callback(...)
except fluidstack.core.ApiError as e: # Handle all errors
  print(e.status_code)
  print(e.body)
```

## Advanced

### Timeouts

By default, requests time out after 60 seconds. You can configure this with a
timeout option at the client or request level.

```python
from fluidstack.client import FluidStack

client = FluidStack(
    ...,
    # All timeouts are 20 seconds
    timeout=20.0,
)

# Override timeout for a specific method
client.auth.get_callback(..., {
    timeout_in_seconds=20.0
})
```

### Retries

The SDK is instrumented with automatic retries with exponential backoff. A request will be
retried as long as the request is deemed retriable and the number of retry attempts has not grown larger
than the configured retry limit (default: 2).

A request is deemed retriable when any of the following HTTP status codes is returned:

- [408](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/408) (Timeout)
- [429](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429) (Too Many Requests)
- [5XX](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/500) (Internal Server Errors)

Use the `max_retries` request option to configure this behavior.

```python
client.auth.get_callback(..., {
     max_retries=1
})
```

### Custom HTTP client

You can override the httpx client to customize it for your use-case. Some common use-cases
include support for proxies and transports.

```python
import httpx

from fluidstack.client import FluidStack

client = FluidStack(...,
    http_client=httpx.Client(
        proxies="http://my.test.proxy.example.com",
        transport=httpx.HTTPTransport(local_address="0.0.0.0"),
    ),
)
```

## Beta Status

This SDK is in **Preview**, and there may be breaking changes between versions without a major
version update.

To ensure a reproducible environment (and minimize risk of breaking changes), we recommend pinning a specific package version.

## Contributing

While we value open-source contributions to this SDK, this library is generated programmatically.
Additions made directly to this library would have to be moved over to our generation code,
otherwise they would be overwritten upon the next generated release. Feel free to open a PR as
a proof of concept, but know that we will not be able to merge it as-is. We suggest opening
an issue first to discuss with us!

On the other hand, contributions to the README are always very welcome!
