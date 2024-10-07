Vagrant.configure("2") do |config|
    config.vm.box = "bento/ubuntu-22.04"
    config.vm.box_check_update = false
    
    
    config.vm.define "app" do |node|

        node.vm.provider "virtualbox" do |vb|
            vb.name = "app"
            vb.memory = 2048
            vb.cpus = 2
        end    
        node.vm.hostname = "app"
        node.vm.network "private_network", ip: "10.10.10.10"
        node.vm.network "forwarded_port", guest: 22, host: "2711", auto_correct: true
        node.vm.provision "setup-hosts", :type => "shell", :path => "setup-hosts.sh" do |s|
            s.args = ["enp0s8"]
        end
    end
end
########################################################
Vagrant.configure("2") do |config|
    config.vm.box = "bento/ubuntu-22.04"
    config.vm.box_check_update = false
    config.vm.define "web" do |node|
        node.vm.provider "virtualbox" do |vb|
            vb.name = "web"
            vb.memory = 2048
            vb.cpus = 2
        end    
        node.vm.hostname = "web"
        node.vm.network  "private_network", ip: "10.10.10.20"
        node.vm.network "forwarded_port", guest: 22, host: "2714", auto_correct: true
        node.vm.provision "setup-hosts", :type => "shell", :path => "setup-hosts.sh" do |s|
            s.args = ["enp0s8"]
        end
    end
end
##############################################################
Vagrant.configure("2") do |config|
    config.vm.box = "bento/ubuntu-22.04"
    config.vm.box_check_update = false
    config.vm.define "db" do |node|
        node.vm.provider "virtualbox" do |vb|
            vb.name = "db"
            vb.memory = 2048
            vb.cpus = 2
        end    
        node.vm.hostname = "db"
        node.vm.network "private_network", ip: "10.10.10.30"
        node.vm.network "forwarded_port", guest: 22, host: "2718", auto_correct: true
        node.vm.provision "setup-hosts", :type => "shell", :path => "setup-hosts.sh" do |s|
            s.args = ["enp0s8"]
        end
    end
end
