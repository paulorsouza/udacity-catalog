# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial32"
  config.vm.synced_folder ".", "/vagrant"
  config.vm.network "forwarded_port", guest: 8000, host: 8000, host_ip: "127.0.0.1"
  config.vm.network "forwarded_port", guest: 5000, host: 5000, host_ip: "127.0.0.1"

  config.vm.provision "shell", inline: <<-SHELL
    apt-get -qqy update
    apt-get -qqy upgrade
    apt-get -qqy install make zip unzip postgresql

    apt-get -qqy install python3 python3-pip
    sudo pip3 install --upgrade pip
    sudo pip3 install flask packaging oauth2client redis passlib flask-httpauth
    sudo pip3 install sqlalchemy flask-sqlalchemy psycopg2-binary bleach requests
    sudo pip3 install -U pytest

    su postgres -c 'createuser -dRS vagrant'
    su vagrant -c 'createdb catalog'
    su vagrant -c 'psql -d catalog -f /vagrant/sql/drop.sql'
    su vagrant -c 'psql -d catalog -f /vagrant/sql/create.sql'

    vagrantTip="[35m[1mThe shared directory is located at /vagrant\\nTo access your shared files: cd /vagrant[m"
    echo -e $vagrantTip > /etc/motd
    echo "Done installing your virtual machine!"
  SHELL
end