local android_device = os.getenv("ANDROID_DEVICE_NAME")

require("flutter-tools").setup_project({
	{
		name = "Web",
		device = "web-server",
		web_port = "8080",
		flutter_mode = "debug",
		additional_args = { "--wasm" },
	},
	{
		name = "Linux",
		device = "linux",
	},
	{
		name = "Android physical",
		device = android_device,
	},
})
