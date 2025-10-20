# Pi Security Camera

A project about a remote Raspberry Pi security camera.

## Main dependencies

- FastAPI
  - Includes Pydantic
- Requests for the Raspberry Pi (not installed yet)

## Structure

```mermaid
flowchart TD
    pi_camera[Pi device] --> server[Server]
    server[Server] --> pi_camera[Pi device]

    server --> client["Client (e.g. smartphone)"]
    client --> server
```
