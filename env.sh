#!/bin/bash
source ~/.profile
source ~/.bashrc

function info() { echo -e "\e[34m[INFO]\e[0m $1"; }

function install_packages() {
    info "setup apt source"
    wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -
    sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'

    sudo apt-get update

    info "install jenkins"
    sudo apt-get install jenkins

    info "install basic packages"
    sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm git

    info "install sqlite"
    sudo apt-get install -y sqlite3 libsqlite3-dev
}

function install_pyenv() {
    rm -rf ~/.pyenv

    info "install pyenv"
    git clone https://github.com/yyuu/pyenv.git ~/.pyenv

    info "setup environment"
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
    echo 'eval "$(pyenv init -)"' >> ~/.profile

    source ~/.profile
}

function install_python(){
    info "install python 3.4.1"
    pyenv install 3.4.1
    pyenv versions

    info "switch python version"
    pyenv local 3.4.1
    pyenv version
    python --version
}

function install_pip() {
    info "install pip"
    wget https://bootstrap.pypa.io/get-pip.py
    python get-pip.py
    pip install -U pip
}

function install_pip_packages(){
    info "install pip packages"
    pip install coverage nose pylint

    info "install behave"
    pip install behave
    pip install -U behave

    info "install django"
    pip install Django==1.9.7
    pip install behave-django
    pip install pyparsing
}

function install_virtualenv(){
    info "install virtualenv"
    git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
    pip install virtualenv

    info "setup virtualevn"
    mkdir -p ${HOME}/myWorkspace/venv

    virtualenv ${HOME}/myWorkspace/venv
    source ${HOME}/myWorkspace/venv/bin/activate

    echo "source ${HOME}/myWorkspace/venv/bin/activate" >> ~/.bashrc
}

function setup(){
    case "$1" in
        apt-pkg)
            install_packages
            ;;
        pyenv)
            install_pyenv
            ;;
        python)
            install_python
            ;;
        pip)
            install_pip
            ;;
        pip-pkg)
            install_pip_packages
            ;;
        virtualenv)
            install_virtualenv
            ;;
        all)
            install_packages
            install_pyenv
            install_python
            install_pip
            install_pip_packages
            install_virtualenv
            ;;
        *)
            echo "Usage $0 apt-pkg|pyenv|python|pip|pip-pkg|virtualenv|all"
            exit 1
    esac
}

if [ $# == 0 ]; then setup help; fi
for opt in $*; do setup $opt; done
