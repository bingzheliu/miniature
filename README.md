# Miniature

<!-- [![Build Status](https://travis-ci.org/containernet/containernet.svg?branch=master)](https://travis-ci.org/containernet/containernet) -->

## Miniature: Containernet fork that allows to use Kubernete cluster nodes as hosts in emulated networks

Miniature leverage [Kind](https://kind.sigs.k8s.io/) to bootstrap kubernetes clusters, where each container represent a kubernete node. These containers are connect through Containernet to construct emulated networks. 

The features that are supported by [Containernet](https://github.com/containernet/containernet) are also supported in Miniature. 

* Kind website: https://kind.sigs.k8s.io/
* Containernet website: https://containernet.github.io/
* Mininet website:  http://mininet.org
* Original Mininet repository: https://github.com/mininet/mininet

<!-- ## Cite this work

If you use Containernet for your research and/or other publications, please cite (beside the original Mininet paper) the following paper to reference our work:

M. Peuster, H. Karl, and S. v. Rossem: [**MeDICINE: Rapid Prototyping of Production-Ready Network Services in Multi-PoP Environments**](http://ieeexplore.ieee.org/document/7919490/). IEEE Conference on Network Function Virtualization and Software Defined Networks (NFV-SDN), Palo Alto, CA, USA, pp. 148-153. doi: 10.1109/NFV-SDN.2016.7919490. (2016)

Bibtex:

```bibtex
@inproceedings{peuster2016medicine, 
    author={M. Peuster and H. Karl and S. van Rossem}, 
    booktitle={2016 IEEE Conference on Network Function Virtualization and Software Defined Networks (NFV-SDN)}, 
    title={MeDICINE: Rapid prototyping of production-ready network services in multi-PoP environments}, 
    year={2016}, 
    volume={}, 
    number={}, 
    pages={148-153}, 
    doi={10.1109/NFV-SDN.2016.7919490},
    month={Nov}
}
``` -->

<!-- ## NFV multi-PoP Extension: `vim-emu`

There is an extension of Containernet called [vim-emu](https://github.com/containernet/vim-emu) which is a full-featured multi-PoP emulation platform for NFV scenarios. Vim-emu was developed as part of the [SONATA-NFV](http://www.sonata-nfv.eu) project and is now hosted by the [OpenSource MANO project](https://osm.etsi.org/). -->

---
## Features

* Add a Kubernete cluster (currently only supporting Kind) to Mininet topologies

Following are what supported by Containernet
* Add, remove Docker containers to Mininet topologies
* Connect Docker containers to topology (to switches, other containers, or legacy Mininet hosts)
* Execute commands inside containers by using the Mininet CLI
* Dynamic topology changes
   * Add hosts/containers to a *running* Mininet topology
   * Connect hosts/docker containers to a *running* Mininet topology
   * Remove Hosts/Docker containers/links from a *running* Mininet topology
* Resource limitation of Docker containers
   * CPU limitation with Docker CPU share option
   * CPU limitation with Docker CFS period/quota options
   * Memory/swap limitation
   * Change CPU/mem limitations at runtime!
* Expose container ports and set environment variables of containers through Python API
* Traffic control links (delay, bw, loss, jitter)
* Automated installation based on Ansible playbook

## Installation

### Install Containernet
Automatic installation is provided through an Ansible playbook.

Requires: **Ubuntu Linux 18.04 LTS** and **Python3**
Experimental: **Ubuntu Linux 20.04 LTS** and **Python3**

```bash
$ sudo apt-get install ansible git aptitude
$ git clone https://github.com/violetbingzhe/miniature
$ cd miniature/ansible
$ sudo ansible-playbook -i "localhost," -c local install.yml
$ cd ..
```
    
Wait (and have a coffee) ...

You can switch between development (default) and normal installation as follows:

```sh
sudo make develop
# or 
sudo make install
```

### Install Kind
Follow instruction from here: https://github.com/kubernetes-sigs/kind

## Examples

### Usage example 

Start example topology with one Docker container and two kubernetes nodes connected to the network.

* run: `sudo python3 kube_example_kind.py`

### Topology example

In your custom topology script you can add kubernete cluster like this:

```python
net = KubeSim(controller=Controller)
info('*** Adding docker containers\n')
# config is optional
net.addKubeCluster("test", config = "config/kind.yaml")
# adding a control plane node
k1 = net.addKubeNode("test", "k1", role = "control-plane", type = "kind")
# adding a worker node
k2 = net.addKubeNode("test", "k2", role = "worker", type = "kind")
# can add a docker container into the topology
d1 = net.addDocker('d1', ip='172.18.0.10', dimage="ubuntu:trusty")
```

For more features, you could find it on Mininet or Containernet website. 

## Documentation
More details TBD.
<!-- Containernet's [documentation](https://github.com/containernet/containernet/wiki) can be found in the [GitHub wiki](https://github.com/containernet/containernet/wiki). The documentation for the underlying Mininet project can be found [here](http://mininet.org/).
 -->
## Contact
### Developer

Bingzhe Liu
* Mail: <bingzhe (at) illinois (dot) edu>
