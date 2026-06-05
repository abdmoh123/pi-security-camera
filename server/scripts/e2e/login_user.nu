#!/usr/bin/env nu

(
    open data/user_login.json
    | http post http://localhost:8000/api/v0/auth/token --content-type multipart/form-data $in
    | tee { to json | save res/user_token.json --force }
)
