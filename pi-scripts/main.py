from typing import Annotated
import typer

import uvicorn

app = typer.Typer()


@app.command()
def serve(reload: Annotated[bool, typer.Option()] = False) -> None:
    uvicorn.run("main:app", reload=reload)


if __name__ == "__main__":
    app()
