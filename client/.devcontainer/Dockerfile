# syntax=docker/dockerfile:1

FROM docker.io/fedora:43

ARG USER_UID=1000
ARG USER_GID=1000

# Installs development tools such as neovim (text editor)
RUN <<EOF
dnf copr enable dejan/lazygit -y
dnf update -y
dnf install -y git git-lfs lazygit neovim ripgrep fd-find fzf unzip wget
EOF

# Install github cli
RUN <<EOF
sudo dnf install -y dnf5-plugins
sudo dnf config-manager addrepo --from-repofile=https://cli.github.com/packages/rpm/gh-cli.repo
sudo dnf install gh -y --repo gh-cli
EOF

ENV ANDROID_SDK_ROOT=~/SDKs/Android
ENV ANDROID_HOME=~/SDKs/Android

# Download and install Android Command Line Tools
RUN mkdir -p ${ANDROID_HOME}/cmdline-tools \
    && wget -O commandlinetools.zip "https://dl.google.com/android/repository/commandlinetools-linux-8512546_latest.zip" \
    && unzip commandlinetools.zip -d ${ANDROID_HOME}/cmdline-tools \
    && mv ${ANDROID_HOME}/cmdline-tools/cmdline-tools ${ANDROID_HOME}/cmdline-tools/latest \
    && rm commandlinetools.zip

# Add Android SDK stuff to path
ENV PATH="${PATH}:${ANDROID_HOME}/cmdline-tools/latest/bin:${ANDROID_HOME}/platform-tools:${ANDROID_HOME}/emulator"
