#!/usr/bin/env nu

let token = (open res/user_token.json | get access_token)
let user_id = (open res/user.json | get id)
http get $"http://localhost:8000/api/v0/users/($user_id)/videos" --headers { Authorization: $"Bearer ($token)" } | to json | tee { save res/videos.json --force }
