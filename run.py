import os
import sys

import uvicorn
from fastapi import HTTPException


async def _run_server():
    # Get Config Path
    config_dir_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config'))

    # Add To PATH Config Dir
    sys.path.append(config_dir_path)

    from config.logger import logger

    try:
        from config.test_app import test_main_route

        await test_main_route()
        logger.info("The application test has been successfully executed")
    except Exception as e:
        logger.error(f"An error occurred when running tests | {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred when running tests | {e}")

    uvicorn_cmd = "app:app"
    uvicorn.run(uvicorn_cmd, host="0.0.0.0", port=8080, reload=True)


if __name__ == "__main__":
    import asyncio

    asyncio.run(_run_server())
