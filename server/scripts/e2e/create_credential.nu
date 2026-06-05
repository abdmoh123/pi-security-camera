#!/usr/bin/env nu

let token = (open res/user_token.json | get access_token)
http post http://localhost:8000/api/v0/users/1/credential --headers { Authorization: $"Bearer ($token)" } "" | tee { to json | save res/credential.json }
