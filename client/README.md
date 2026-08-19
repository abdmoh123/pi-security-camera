# Pisec client app

A flutter-based project for interacting with the pisec server.

> [!NOTE]
> This client is not the same as the client application running on the cameras.
> That is part of the camera module.

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
