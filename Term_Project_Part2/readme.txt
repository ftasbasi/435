//Furkan TAŞBAŞI
//Batuhan BAT

-----------------------------------------------------------------------------------------------

How to run:
Put source.py onto machine s and type 'python source.py'
Put broker.py onto machine B and type 'python broker.py'
Put destination.py onto machine d and type 'python destination.py'

*** RUN SOURCE AT THE END ***

-----------------------------------------------------------------------------------------------
!!!!!!    All experiment datas are given in "delay_experiments.xlsx" file.    !!!!!

Example Experiment Operations

sudo tc qdisc change dev ens6 root netem loss 0% corrupt 0% duplicate 0% delay 3ms reorder 35% 50%

Example Routing Command
ip route add 10.10.5.2/32 via 10.10.5.1 dev ens7

Routing Kernel Forwarding Config File
vi /etc/sysctl.conf

Before doing any experiment we syncronized all devices via "ntp" command as the following :
	"sudo ntpdate -s time.nist.gov"
Then we checked any possible difference with the following command (we checked differences for all devices) :
	"clockdiff -o 10.10.1.1" 

After validating there is no difference we started doing experiments.

For any possible port kill necessity, we have used a basic script named fuser.sh included in out howework folder.
