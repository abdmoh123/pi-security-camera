require("flutter-tools").setup_project({
	{
		name = "Web",
		device = "web-server",
		web_port = "8080",
		flutter_mode = "debug",
		additional_args = { "--wasm" },
	},
})
