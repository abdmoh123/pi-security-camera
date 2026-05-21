#!/usr/bin/env nu

let token = (open res/credential_token.json | get access_token)
open data/camera.json | to json | http post http://localhost:8000/api/v0/cameras/ $in --headers { Authorization: $"Bearer ($token)" } | to json | tee { save res/camera.json }
