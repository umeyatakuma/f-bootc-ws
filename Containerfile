FROM quay.io/fedora/fedora-bootc                     

WORKDIR /app

RUN sudo dnf -y install swayidle sway-wallpapers swaybg swaylock sway-systemd sway sway-config-upstream waybar
RUN sudo dnf -y install fcitx5 fcitx5-mozc fcitx5-configtool
RUN sudo dnf -y install tlp tlp-rdw
RUN sudo dnf -y install virt-viewer
RUN sudo dnf -y install distrobox
RUN sudo dnf -y install firefox
RUN sudo dnf -y install light pavucontrol playerctl pulseaudio-utils gammastep 
RUN sudo dnf -y install langpacks-fonts-ja langpacks-fonts-en 
RUN sudo dnf -y remove ffmpeg-free libswresample-free
RUN sudo dnf -y install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
RUN sudo dnf -y install https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
RUN sudo dnf -y install ffmpeg
RUN sudo dnf -y install krb5-workstation
RUN dnf -y install flatpak
RUN dnf -y clean all

RUN echo "flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo" > install.sh
RUN echo "flatpak -y install com.github.d4nj1.tlpui" >> install.sh
RUN echo "flatpak -y install com.nextcloud.desktopclient.nextcloud" >> install.sh
RUN echo "flatpak -y install com.slack.Slack" >> install.sh
RUN echo "flatpak -y install org.mozilla.vpn" >> install.sh
RUN echo "flatpak -y install im.riot.Riot" >> install.sh
RUN echo "flatpak -y install com.bitwarden.desktop" >> install.sh
RUN echo "flatpak -y install org.libreoffice.LibreOffice" >> install.sh

RUN echo "sudo rpm-ostree kargs --append-if-missing=quiet" >> install.sh

