all: install_dependecies install copy_scripts

install_dependecies: 
	sudo apt-get install libpcre3-dev libssl-dev zlib1g-dev libjpeg62-dev libreadline5-dev readline-common libxml2-dev

install:
	./install.sh --password="senha_do_portal" zeo

copy_scripts: startCluster.sh stopCluster.sh restartCluster.sh
	cp startCluster.sh stopCluster.sh restartCluster.sh /home/herman/Plone/zeocluster
