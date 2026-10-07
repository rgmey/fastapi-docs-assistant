# try #1

 uv run fastapi-docs-assistant "How do I declare a path parameter in FastAPI?"
2026-10-08 02:04:07,227 INFO httpx2: HTTP Request: POST https://openrouter.ai/api/v1/chat/completions "HTTP/1.1 200 OK"
2026-10-08 02:04:30,008 INFO fastapi_docs_assistant.llm: LLM call model=openai/gpt-5-nano in=17 out=1974 latency=24.20s
You declare a path parameter by including a dynamic segment in the route path and then adding a function parameter with the same name (typed for validation).

Key points:
- Put the parameter in the path, inside curly braces: /items/{item_id}
- In the path operation function, declare a parameter named item_id with a type hint
- FastAPI will parse/validate it (e.g., convert to int) and return a 422 if invalid
- You can add extra validation/metadata with Path(...)

Examples:

- Basic path parameter (no extra validation)
  from fastapi import FastAPI

  app = FastAPI()

  @app.get("/items/{item_id}")
  async def read_item(item_id: int):
      return {"item_id": item_id}

- With extra validation/metadata
  from fastapi import FastAPI, Path

  app = FastAPI()

  @app.get("/items/{item_id}")
  async def read_item(
      item_id: int = Path(..., title="The ID of the item", ge=1)
  ):
      return {"item_id": item_id}

- Multiple path parameters
  @app.get("/users/{user_id}/posts/{post_id}")
  async def read_post(user_id: int, post_id: int):
      return {"user_id": user_id, "post_id": post_id}

- Using an enum for restricted values
  from enum import Enum

  class Category(str, Enum):
      book = "book"
      pen = "pen"

  @app.get("/items/{category}")
  async def list_by_category(category: Category):
      return {"category": category}

Note:
- Path parameters are required and must appear in the URL. If you need optional values, use query parameters (with a default) instead of path parameters.













# try #2
 uv run fastapi-docs-assistant "How do I declare a path parameter in FastAPI?"
2026-10-08 02:13:27,668 INFO httpx2: HTTP Request: POST https://openrouter.ai/api/v1/chat/completions "HTTP/1.1 200 OK"
2026-10-08 02:13:52,031 INFO fastapi_docs_assistant.llm: LLM call model=openai/gpt-5-nano in=17 out=2430 latency=25.45s
In FastAPI, path parameters are pieces of the URL pathdefined with braces in the route, and you expose them in the handler function with a parameter of the same name (typed for validation).

Basic example:
- Route with a path parameter item_id of type int
- Handler param item_id: int

Code:
- from fastapi import FastAPI
- app = FastAPI()

- @app.get("/items/{item_id}")
- async def read_item(item_id: int):
-     return {"item_id": item_id}

Notes:
- The function parameter name must match the placeholder in the path.
- The type annotation enables automatic validation andconversion (e.g., int, UUID, str).

More examples:
- Multiple path parameters
  - @app.get("/users/{user_id}/orders/{order_id}")
  - async def read_order(user_id: int, order_id: int):
  -     return {"user_id": user_id, "order_id": order_id}

- With extra validation/metadata using Path
  - from fastapi import Path
  - @app.get("/items/{item_id}")
  - async def read_item(item_id: int = Path(..., title="The ID of the item", ge=1)):
  -     return {"item_id": item_id}

- Using a non-number type (e.g., UUID)
  - from uuid import UUID
  - @app.get("/users/{user_id}")
  - async def read_user(user_id: UUID):
  -     return {"user_id": str(user_id)}

Important:
- Path parameters are required; you cannot make a pathparam optional by giving it a default value. If you need optional data, use query parameters instead.

