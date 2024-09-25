import asyncio

import uvicorn

from apps.aletheia.api.main import init_db


if __name__ == '__main__':
    asyncio.run(init_db())
    uvicorn.run("apps.api.main:api", host="0.0.0.0", port=8000, reload=True)
