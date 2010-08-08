bin/poundctl stop
killall varnishd
bin/plonectl stop

bin/poundrun
bin/varnish-instance
bin/plonectl start
