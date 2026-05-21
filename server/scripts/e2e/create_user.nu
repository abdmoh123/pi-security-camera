#!/usr/bin/env nu

open data/user.json | to json | http post http://localhost:8000/api/v0/users/ $in | to json | tee { save res/user.json }
