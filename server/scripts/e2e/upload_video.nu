#!/usr/bin/env nu

let file_name = "video-2024-08-25_00-41-04.mp4"

let token = (open res/credential_token.json | get access_token)

(curl -X POST http://localhost:8000/api/v0/videos/
  -H $'Authorization: Bearer ($token)'
  -F $'file_name=($file_name)'
  -F $'video_file=@./($file_name);type=video/mp4'
) | from json
