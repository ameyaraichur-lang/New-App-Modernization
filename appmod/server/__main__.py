"""python -m appmod.server — serve the Pipeline Console + API on :8600."""

import uvicorn

if __name__ == "__main__":
    uvicorn.run("appmod.server.api:app", host="127.0.0.1", port=8600, log_level="info")
