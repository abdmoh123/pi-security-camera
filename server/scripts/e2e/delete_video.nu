#!/usr/bin/env nu

let token = (open res/user_token.json | get access_token)
let videos = open res/videos.json
let first_video = $videos | first
http delete $"http://localhost:8000/api/v0/videos/($first_video.id)" --headers { Authorization: $"Bearer ($token)" }
