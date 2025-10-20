# Pi Security Camera

A project about a remote Raspberry Pi security camera.

## Main dependencies

- FastAPI
  - Includes Pydantic
- Requests for the Raspberry Pi (not installed yet)

## Structure

```mermaid
flowchart TD
    pi_camera[Pi device] <-->|Requests| server[Server]

    server <-->|FastAPI| client["Client (e.g. smartphone)"]
```
