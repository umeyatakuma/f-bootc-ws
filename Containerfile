FROM quay.io/fedora/fedora-bootc                     

WORKDIR /app

RUN sudo dnf -y install \
    swayidle \
    sway-wallpapers \
    swaybg \
    swaylock \ 
    sway-systemd \
    sway \
    sway-config-upstream \ 
    waybar \
    dmenu \
    dunst \
    light \
    pavucontrol \
    playerctl \
    pulseaudio-utils \
    gammastep \
    rsync \
    cronie \
    cups \
    sox \
    fprintd \
    fprintd-pam \
    iwlwifi-mvm-firmware \
    NetworkManager-wifi \
    NetworkManager-openvpn \
    openvpn \
    pkcs11-helper \
    langpacks-fonts-ja \
    langpacks-fonts-en \
    krb5-workstation \
    glibc-langpack-en \
    gnome-keyring \ 
    fcitx5 \
    fcitx5-mozc \
    fcitx5-configtool \ 
    tlp \
    tlp-rdw \
    virt-viewer \
    distrobox \
    firefox \
    git \
    vim-enhanced \
    man-db \
    grim \
    flatpak \
    fedora-repos-ostree
RUN sudo dnf -y remove nano-default-editor

RUN sudo dnf -y remove ffmpeg-free libswresample-free
RUN sudo dnf -y install \
    https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm \
    https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
RUN sudo dnf -y install ffmpeg

RUN dnf -y clean all
Run bootc container lint
