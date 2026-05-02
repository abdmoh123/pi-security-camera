# syntax=docker/dockerfile:1

FROM docker.io/fedora:43

ARG USER_UID=1000
ARG USER_GID=1000

# Installs development tools such as neovim (text editor)
RUN <<EOF
dnf copr enable dejan/lazygit -y
dnf update -y
dnf install -y git git-lfs lazygit neovim ripgrep fd-find fzf
EOF

# Install github cli
RUN <<EOF
sudo dnf install -y dnf5-plugins
sudo dnf config-manager addrepo --from-repofile=https://cli.github.com/packages/rpm/gh-cli.repo
sudo dnf install gh -y --repo gh-cli
EOF

# Setup environment variables for uv
ENV PATH="/root/.local/bin:${PATH}"
ENV PATH="/root/.local/share/uv/python:${PATH}"

# Install and setup project with mise
RUN <<EOF
mise trust && mise init
EOF
