# Third-Party
import uvicorn

# Local
from src.settings.base import app


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)

    