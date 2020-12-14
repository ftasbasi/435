//Furkan TAŞBAŞI
//Batuhan BAT

-----------------------------------------------------------------------------------------------

How to run:
Put client.py onto machine s and type 'python client.py'
Put broker.py onto machine B and type 'python broker.py'
Put router1.py onto machine r1 and type 'python router1.py'
Put router2.py onto machine r2 and type 'python router2.py'
Put destination.py onto machine d and type 'python destination.py'

*** RUN CLIENT AT THE END ***

-----------------------------------------------------------------------------------------------
!!!!!!    All experiment data is given in "delay_experiments.xlsx" file.    !!!!!

Delay Experiment Operations

Before doing any experiment we syncronized all devices via "ntp" command as the following :
	"sudo ntpdate -s time.nist.gov"
Then we checked any possible difference with the following command (we checked differences for all devices) :
	"clockdiff -o 10.10.1.1" 

After validating there is no difference we started doing experiments.

To do "network emulation delay and the end-to-end delay experiment" 

We found correct interface names via using "ifconfig" command (it also can be seen on GENI platform by clicking all devices separately and finding interface names)

Example configuration commands for necessary devices are given as the following explanation:
(Using Experiment 3)

BROKER device interfaces to apply delay configuration

	tc qdisc add dev eth1 root netem delay 60ms 5ms distribution normal
	tc qdisc add dev eth2 root netem delay 60ms 5ms distribution normal
	tc qdisc add dev eth3 root netem delay 60ms 5ms distribution normal

ROUTER1 device interfaces to apply delay configuration

	tc qdisc add dev eth1 root netem delay 60ms 5ms distribution normal
	tc qdisc add dev eth2 root netem delay 60ms 5ms distribution normal

ROUTER2 device interfaces to apply delay configuration

	tc qdisc add dev eth1 root netem delay 60ms 5ms distribution normal
	tc qdisc add dev eth2 root netem delay 60ms 5ms distribution normal

DESTINATION device interfaces to apply delay configuration
	
	tc qdisc add dev eth2 root netem delay 60ms 5ms distribution normal


After doing each experiment we removed the configuration and step forward for next experiment
Removing existing delay configuration for an interface "eth1" (example)
	
	tc qdisc del dev eth1 root netem

