#!groovy

import jenkins.model.*
import hudson.security.*
import hudson.util.*

def instance = Jenkins.getInstance()
def pm = instance.getPluginManager()
def uc = instance.getUpdateCenter()

def plugins = [
  'git', 'workflow-aggregator', 'blueocean'  // List your plugins here
]

plugins.each {
  if (!pm.getPlugin(it)) {
    def plugin = uc.getPlugin(it)
    if (plugin) {
      plugin.deploy()
    }
  }
}

instance.save()