# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial32"
  config.vm.synced_folder ".", "/vagrant"

  config.vm.provision "shell", inline: <<-SHELL
    apt-get -qqy update
    apt-get -qqy upgrade
    apt-get -qqy install make zip unzip postgresql

    apt-get -qqy install python3 python3-pip
    sudo pip3 install --upgrade pip
    sudo pip3 install texttable psycopg2 psycopg2-binary
    sudo pip3 install -U pytest

    su postgres -c 'createuser -dRS vagrant'
    su vagrant -c 'createdb'
    su vagrant -c 'createdb news'

    vagrantTip="[35m[1mThe shared directory is located at /vagrant\\nTo access your shared files: cd /vagrant[m"
    echo -e $vagrantTip > /etc/motd
    echo "Done installing your virtual machine!"
    
    wget https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip
    unzip newsdata.zip
    su vagrant -c 'psql news -f newsdata.sql'

  SHELL
end