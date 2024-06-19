# Third-Party
import uvicorn

# Local
from src.settings.base import app
from src.apps.users.views import admins, users


app.include_router(router=admins.router)
app.include_router(router=users.router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)

    