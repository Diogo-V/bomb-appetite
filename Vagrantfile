# -*- mode: ruby -*-
# vi: set ft=ruby :

# Ensure this Project is for Virtualbox Provider
ENV['VAGRANT_DEFAULT_PROVIDER'] = "virtualbox"

VAGRANT_PLUGINS = [
  "vagrant-vbguest"
]

VAGRANT_PLUGINS.each do |plugin|
  unless Vagrant.has_plugin?("#{plugin}")
    system("vagrant plugin install #{plugin}")
    exit system('vagrant', *ARGV)   
  end
end

Vagrant.configure("2") do |config|
  config.vm.boot_timeout = 2400
  config.ssh.insert_key = false
  config.vbguest.auto_update = false
  config.vm.box_check_update = false

  # create db node
  config.vm.define "db" do |db|
    db.vm.box = "ubuntu/focal64"
    db.vm.hostname = "db"
    db.vm.network "private_network", ip: "192.168.0.1", virtualbox__intnet: "sw-1"
    db.vm.provision "shell", inline: <<-SHELL
    # Add additional network configuration commands here
    SHELL
    # Provider Virtualbox
    db.vm.provider "virtualbox" do |vb|
      vb.name = "db"
    end # of vb 
    db.vm.provision "shell", path: "services/db/boot/hosts.sh"
    db.vm.provision "shell", path: "services/db/boot/setup_ssl.sh" 
    db.vm.provision "shell", path: "services/db/boot/init.sh"     
    db.vm.provision "shell", path: "services/db/boot/firewall.sh" 
  end # of db

  #TODO: DMZ -> backend

    # create backend node
    config.vm.define "backend" do |backend|
      backend.vm.box = "ubuntu/focal64"
      backend.vm.hostname = "backend"
      backend.vm.network "private_network", ip: "192.168.0.2", virtualbox__intnet: "sw-1"
      backend.vm.network "private_network", ip: "192.168.1.2", virtualbox__intnet: "sw-2"
      backend.vm.provision "shell", inline: <<-SHELL
        # Add additional network configuration commands here
      SHELL
      # Provider Virtualbox
      backend.vm.provider "virtualbox" do |vb|
        vb.name = "backend"
      end # of vb
  
      backend.vm.synced_folder "services/backend", "/home/vagrant/backend", type: "rsync"
      backend.vm.provision "shell", path: "services/backend/boot/hosts.sh" 
      backend.vm.provision "shell", path: "services/backend/boot/setup_ssl.sh" 
      backend.vm.provision "shell", path: "services/backend/boot/init.sh" 
      backend.vm.provision "shell", path: "services/backend/boot/firewall.sh"    

    end # of backend

    # create web node
    config.vm.define "web" do |web|
      web.vm.box = "ubuntu/focal64"
      web.vm.hostname = "web"
      web.vm.network "private_network", ip: "192.168.1.3", virtualbox__intnet: "sw-2"
      web.vm.provision "shell", inline: <<-SHELL      
        # Add additional network configuration commands here
      SHELL
      web.vm.network "forwarded_port", guest: 3000, host: 8080
      # Provider Virtualbox
      web.vm.provider "virtualbox" do |vb|
        vb.name = "web"
      end # of vb

      web.vm.synced_folder "services/web", "/home/vagrant/web", type: "rsync", rsync__exclude: ["node_modules", ".svelte-kit"]
      web.vm.provision "shell", path: "services/web/boot/hosts.sh"   
      web.vm.provision "shell", path: "services/web/boot/setup_ssl.sh" 
      web.vm.provision "shell", path: "services/web/boot/init.sh"     
      web.vm.provision "shell", path: "services/web/boot/firewall.sh"    
    end # of web


end # of config

