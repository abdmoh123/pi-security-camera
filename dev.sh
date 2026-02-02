#!/bin/bash

devcontainer build
devcontainer up --dotfiles-repository=https://github.com/abdmoh123/.dotfiles.git --dotfiles-target-path=~
devcontainer exec bash
