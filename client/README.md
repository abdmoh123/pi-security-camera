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

### Android

You will have to manually install the Android SDK and command line tools. After that, you set the following environment variables:

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

> [!NOTE]
> By default the mise tasks will assume you are running the app on the web, so the android setup is optional.

## Testing

Before testing, you will need to generate the mock stubs. You do this with the following command:

```bash
dart run build_runner build
```

These mock stubs have been added to .gitignore, so you should not commit them to version control.

After building the stubs, you can run the tests with the following command:

```bash
mise run test
```

Or use the `flutter test` command.

> [!TIP]
> If you use `mise test`, it should automatically build the stubs before running the tests.
> You can also build the mocks manually with `mise run setup-mocks`.
