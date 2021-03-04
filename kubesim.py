#!/usr/bin/python

from mininet.net import Containernet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel, debug
from mininet.util import (ipAdd)

from mininet.node import (KindNode)
from subprocess import Popen, PIPE

class KubeSim( Containernet ):
	def __init__(self, **params):
		# call original Containernet.__init__
		Containernet.__init__(self, **params)
		self.kubeCluster = {}
		self.linksNotProcessed = []
		self.clusterName = ""
		self.numController = 0
		self.numWorker = 0

	def addKubeCluster(self, name, **params):
		if name == self.clusterName:
			error("Cluster %s exists!" % name)
		else:
			self.clusterName = name
		#TODO: support multiple cluster, now only 1 supported.
		#TODO: deal with the config file

	def addKubeNode(self, clusterName, name, **params):
		if params.get('type', "kind") != "kind":
			error("Only supporting Kind node now!")
		else:
			params["cls"] = KindNode

		role = params.get("role", "worker")
		cname = clusterName + "-"
		if role == "worker":
			cname = cname + "worker" + ("" if self.numWorker == 0 else str(self.numWorker))
			self.numWorker += 1
		elif role == "control-plane":
			cname = cname + "control-plane" + ("" if self.numController == 0 else str(self.numController))
			self.numController += 1
		else:
			error("Unknown role %s!" % role)

		defaults = {"cname": cname}
		defaults.update( params )

		# TODO: may need to have a sperate IP range than the default ones
		# This IP now is not being used. 
		# user-defined IP is not supported now. 

		self.kubeCluster[name] = self._addKubeNode(name, **defaults)
		return self.kubeCluster[name]

	def start(self):
		# deal with kind
		# Now by default it's kind node, can integrate other kind of node. 
		if len(self.kubeCluster) > 0:
		   self.boostKubeCluster()

		for k in self.kubeCluster:
			self.kubeCluster[k].init()
			# TODO:allowing to add sth other than kind?
			# TODO: make sure the container ID and process ID is get

		for l in self.linksNotProcessed:
			Containernet.addLink(self, l[0], l[1], port1=l[2], port2=l[3], cls=l[4], **l[5])

		Containernet.start(self)

		for k in self.kubeCluster:
			self.kubeCluster[k].bringIntfUp()
			self.kubeCluster[k].setupKube()

	def addLink( self, node1, node2, port1=None, port2=None,
				 cls=None, **params ):
		# delays to add link 
		self.linksNotProcessed.append((node1, node2, port1, port2, cls, params))

	def _addKubeNode(self, name, cls=KindNode, **params):
		"""
		This starts a stub class of KubeNode, and not start a container
		"""
		return self.addHost(name, cls=cls, **params)

	def generateKindConfig(self, name, cluster):
		s = "kind: Cluster\n\
apiVersion: kind.x-k8s.io/v1alpha4\n\
nodes: \n"

		for k in cluster:
			s = s + "- role: " + cluster[k].role + "\n"

		configPath = "config/kubsim_cluster_"+name+".yaml"
		with open(configPath,"w") as f:
			f.write(s)

		info("** Kind Config Created **\n")
		return configPath

	def boostKubeCluster(self):
		# Get cluster infomaiton
		info("** Bootstrapping Kind Cluster **\n")
		info("Number of workers %s\nNumber of control-plane %s\n" % (self.numWorker, self.numController))

		if self.numController == 0:
			error("No control plane for kubernetes cluster!")

		 # TODO: enforce certain resource limits
		configPath = self.generateKindConfig(self.clusterName, self.kubeCluster)

		debug(self.pexec(["kind", "create", "cluster", "--name", self.clusterName, 
							"--config", configPath]))
		# TODO: need to parse the output of kind to make sure it's created
		info("**Cluster created successfully!**")

	def pexec( self, cmd ):
		"""Execute a command using popen
		   returns: out, err, exitcode"""
		popen = Popen( cmd, stdout=PIPE, stderr=PIPE)
		# Warning: this can fail with large numbers of fds!
		out, err = popen.communicate()
		exitcode = popen.wait()
		return cmd, out, err, exitcode

