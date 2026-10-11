# Pisec client app

A flutter-based project for interacting with the pisec server.

> [!NOTE]
> This client is not the same as the client application running on the cameras.
> That is part of the camera module.

## Setup

Run `mise restore` to install the required dependencies. Or you could use `flutter pub get`.

> [!NOTE]
> You will need to run `mise install` to install all the required tooling to run the mise tasks.
> Alternatively, you can manually install the required tools and dependencies and the run commands yourself.

### Linux

You will need to install extra dependencies using your package manager because mise isn't able to.
The following steps are for a fedora-based system:

```bash
sudo dnf install -y clang libsecret-devel jsoncpp-devel pkg-conf-pkg-config gtk3-devel
```

The rest of the required tools should be installed by mise via `mise install`.

### Android

You can use the `mise run install-android-tools` task to install the android SDK and tools using the android-cli.
Before that, you can set the following environment variables to choose where the SDKs are stored:

- ANDROID_HOME
- ANDROID_SDK_ROOT

By default these env variables are set to `~/Android`, but you can override them in a `.mise.local.toml` file.

An example .mise.local.toml file can be seen below:

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

## Testing

Before testing, you will need to generate the mock stubs. You can do this with the following command:

```bash
dart run build_runner build
```

Or use the mise task:

```bash
mise run setup-mocks
```

These mock stubs have been added to .gitignore, so you should not commit them to version control.

After building the stubs, you can run the tests with the following command:

```bash
mise run test
```

Or use the `flutter test` command.
