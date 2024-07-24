import os
import subprocess
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
        # Run pytest for Testing FastAPI APP Status and DB Users Status
        subprocess.run(["pytest"])

        logger.info("The application test has been successfully executed")
    except Exception as e:
        logger.error(f"An error occurred when running tests | {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred when running tests | {e}")

    # Run FastAPI Application
    uvicorn_cmd = "app:app"
    uvicorn.run(uvicorn_cmd, host="0.0.0.0", port=8080, reload=True)


if __name__ == "__main__":
    import asyncio

    # Run Async Module
    asyncio.run(_run_server())
