#!/usr/bin/env nu

let credential = open res/credential.json
let credential_login = { grant_type: "client_credentials", client_id: $credential.client_id, client_secret: $credential.client_secret }
$credential_login | save credential_login.json
