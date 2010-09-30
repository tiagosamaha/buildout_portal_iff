all: before_install install after_install

before_install: 
	bash helper_scripts/before_install.sh

install:
	./install.sh --password=admin --user=root zeo

after_install:
	bash helper_scripts/after_install.sh
