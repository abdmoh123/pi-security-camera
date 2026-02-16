# Pi Security Camera

A project about a remote Raspberry Pi security camera.

## How to setup

The project can be easily configured using mise. Or you can manually install the required tools and dependencies.

### Client-side

#### Easy setup

You can use `mise install` to partially setup the flutter project. Unfortunately, the android SDK will have to be
installed manually (unless you use [[#Devcontainers]]).
You may also need to set the ANDROID_HOME environment variable to add the SDK and command line tools to your path. The
default value is `~/Android`, but that can be overridden via a `mise.local.toml` file (see example below).

```toml
[env]
ANDROID_HOME = "{{env.HOME}}/SDKs/Android"
ANDROID_SDK_ROOT = "{{env.ANDROID_HOME}}"
_.path = [
    "{{env.ANDROID_HOME}}/cmdline-tools/latest/bin",
    "{{env.ANDROID_HOME}}/platform-tools",
    "{{env.ANDROID_HOME}}/emulator",
]
```

#### Manual setup

Install flutter SDK.
For android development, you will need the Android SDK, which can be installed via Android Studio.

> [!INFO]
> For more information, follow the [official guide](https://docs.flutter.dev/install)

### Server-side (API)

#### Easy setup

The server side of the module can easily be setup using `mise install`. This will install uv with the required version
of python.

#### Manual setup

The server side of the project is still easy to setup without mise. Simply install `uv` following their instructions or
via a package manager. Afterwards, run `uv sync` to install the required dependencies.

## Devcontainers

The project can also be worked on using devcontainers. You can either manually setup the devcontainer or run the `mise
devcontainer` task to do it for you.
The devcontainer will also include mise as well as my own dotfiles for a neovim setup.
