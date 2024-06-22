# Third-Party
import uvicorn

# Local
from src.settings.base import app
from src.apps.users.views import admins, users
from src.apps.events.views import events


app.include_router(router=admins.router)
app.include_router(router=users.router)
app.include_router(router=events.router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)

    