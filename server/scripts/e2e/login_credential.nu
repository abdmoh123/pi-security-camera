#!/usr/bin/env nu

$credential = open res/credential.json
$credential_login = { grant_type: "client_credentials", client_id: $credential.client_id, client_secret: $credential.client_secret }
$credential_login | http post http://localhost:8000/api/v0/auth/camera_token --content-type multipart/form-data $in | to json | tee { save res/credential_token.json --force }
