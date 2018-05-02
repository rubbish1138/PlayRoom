#!/bin/bash

# 18.04向け


HOME=~/


os_settings()
{
    gsettings set org.gnome.desktop.input-sources xkb-options "['ctrl:nocaps']"
    echo "alias emacs='emacs -nw'" >> .bashrc
    source .bashrc
}
japanese_localization()
{
    sudo apt install -y language-pack-ja-base language-pack-ja
    localectl set-locale LANG=ja_JP.UTF-8 LANGUAGE="ja_JP:ja"
    source /etc/default/locale



    # mozc

    if cat /etc/issue | grep '18' ; then
	      # echo "18.04"
	      wget -q -O - http://iij.dl.osdn.jp/users/17/17341/mozc-2.20.2677.102+dfsg-1~ut2-20171008a.tar.xz | tar xJvf -
        cd mozc-*/
        sudo apt install -y qt5-default
    else
	      # echo "16.04"

	      wget -q -O - http://ymu.dl.osdn.jp/users/17/17340/mozc-2.18.2598.102+dfsg-1~ut2-20171008a.tgz | tar xavf -
        cd mozc-*/
        sed -i s/'const bool kActivatedOnLaunch = false;'/'const bool kActivatedOnLaunch = true;'/g mut/src/unix/ibus/property_handler.cc
    fi
    sudo apt install -y clang libdbus-1-dev libglib2.0-dev libgtk2.0-dev subversion tegaki-zinnia-japanese debhelper libibus-1.0-dev build-essential libssl-dev libxcb-xfixes0-dev python-dev gyp protobuf-compiler libqt4-dev libuim-dev libzinnia-dev fcitx-libs-dev devscripts ninja-build devscripts
    
    sudo ./build_mozc_plus_utdict

    tail -n 5 /var/log/apt/history.log | grep Install: | sed -e s/"Install: "// | sed -e s/", automatic"//g | sed -e s/"), "/"\n"/g | sed -e s/" (.*$"/""/g | tr '\n' ' ' | xargs sudo apt-get remove -y

    sudo apt install ./mozc-*.deb ./fcitx-mozc_*.deb ./ibus-mozc_*.deb

    gsettings set org.gnome.settings-daemon.plugins.keyboard active true


}

# emacsのインストール
install_emacs()
{

    sudo apt install -y emacs



}

install_chrome()
{
    yes | sudo wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
    yes | sudo sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
    sudo apt update 
    sudo apt install  google-chrome-stable 
}


sudo apt update -y
sudo apt upgrade -y

os_settings

japanese_localization

install_emacs
install_chrome


echo 'Done.'
