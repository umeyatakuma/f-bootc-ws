FROM quay.io/fedora/fedora-bootc                     

WORKDIR /app

RUN sudo dnf -y install swayidle sway-wallpapers swaybg swaylock sway-systemd sway sway-config-upstream i3status
RUN sudo dnf -y install fcitx5 fcitx5-mozc fcitx5-configtool
RUN sudo dnf -y install virt-viewer
RUN sudo dnf -y install distrobox
RUN sudo dnf -y install firefox
RUN sudo dnf -y install light pavucontrol playerctl pulseaudio-utils gammastep nextcloud libreoffice smplayer audacity
RUN dnf -y install flatpak
RUN dnf -y clean all

RUN echo "flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo" > install.sh
RUN echo "flatpak -y install io.github.seadve.Kooha" >> install.sh
RUN echo "flatpak -y install io.gitlab.librewolf-community" >> install.sh
RUN echo "flatpak -y install us.zoom.Zoom" >> install.sh
RUN echo "flatpak -y install com.github.d4nj1.tlpui" >> install.sh
RUN echo "flatpak -y install com.slack.Slack" >> install.sh
RUN echo "flatpak -y install mozillavpn.flatpak" >> install.sh
RUN echo "flatpak -y install im.riot.Riot" >> install.sh
RUN echo "flatpak -y install com.bitwarden.desktop" >> install.sh
RUN echo "sudo rpm-ostree kargs --append-if-missing=quiet" >> install.sh
RUN echo "sudo cp ./tlp.conf /etc " >> install.sh
COPY tlp.conf .
COPY mozillavpn.flatpak .
