FROM quay.io/fedora/fedora-bootc                     

WORKDIR /app

RUN sudo dnf -y install swayidle sway-wallpapers swaybg swaylock sway-systemd sway sway-config-upstream waybar dmenu gnome-keyring
RUN sudo dnf -y install fcitx5 fcitx5-mozc fcitx5-configtool
RUN sudo dnf -y install tlp tlp-rdw
RUN sudo dnf -y install virt-viewer
RUN sudo dnf -y install distrobox
RUN sudo dnf -y install firefox
RUN sudo dnf -y install light pavucontrol playerctl pulseaudio-utils gammastep 
RUN sudo dnf -y install langpacks-fonts-ja langpacks-fonts-en 
RUN sudo dnf -y install krb5-workstation
RUN sudo dnf -y install rsync cronie fprintd git iwlwifi-mvm-firmware
RUN sudo dnf -y remove ffmpeg-free libswresample-free
RUN sudo dnf -y install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
RUN sudo dnf -y install https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
RUN sudo dnf -y install ffmpeg
RUN dnf -y install flatpak
RUN dnf -y clean all
