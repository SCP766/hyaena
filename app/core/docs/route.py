from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["Docs"])


@router.get(
    path="/elements",
    response_class=HTMLResponse,
    include_in_schema=False,
)
async def stoplight_elements() -> HTMLResponse:
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>API Reference</title>
        <script src="https://unpkg.com/@stoplight/elements/web-components.min.js"></script>
        <link rel="stylesheet" href="https://unpkg.com/@stoplight/elements/styles.min.css" />
    </head>
    <body>
        <elements-api
            apiDescriptionUrl="/openapi.json"
            router="hash"
            layout="sidebar"
        />
    </body>
    </html>
    """

    return HTMLResponse(content=html)
