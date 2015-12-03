# -*- mode: ruby -*-

Vagrant.configure("2") do |config|
  config.vm.box = "trusty64-current"
  config.vm.box_url = "https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box"
  config.vm.synced_folder ".", "/vagrant", nfs: true
  config.ssh.forward_agent = true
  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--memory", "1024"]
  end
  config.vm.define "dev", primary: true do |dev|
    config.vm.network "private_network", ip: "172.16.10.15"
    # nginx
    config.vm.network :forwarded_port, guest: 80, host: 9080
    config.vm.network :forwarded_port, guest: 5000, host: 5001
    config.vm.network :forwarded_port, guest: 5432, host: 5433
    config.vm.provision "ansible" do |ansible|
      ansible.host_key_checking = false
      ansible.extra_vars = { ansible_ssh_user: 'vagrant' }
      ansible.playbook = "provisioning/playbook.yml"
      ansible.inventory_path = "provisioning/development"
      ansible.limit = "all"
    end
  end
end
