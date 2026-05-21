#!/usr/bin/env nu

open data/user_login.json | http post http://localhost:8000/api/v0/auth/token --content-type multipart/form-data $in | to json | tee { save res/user_token.json --force }
