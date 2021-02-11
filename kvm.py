import argparse
import xml.dom.minidom
import os
import urllib.request
import subprocess
import platform

# os.chdir(os.path.realpath(__file__))
java_path = ".\\java6"

parser = argparse.ArgumentParser(description = "APC KVM launcher")
parser.add_argument("jnlp", metavar="JNLP_FILE", type=argparse.FileType('r'),
                    help="The JNLP file downloaded from the KVM to start a session (.JNLP)")
args = parser.parse_args()

jnlp_xml = args.jnlp.read().strip()
DOMTree = xml.dom.minidom.parseString(jnlp_xml)

codebase = DOMTree.getElementsByTagName("jnlp")[0].attributes["codebase"].value + "/"

jars = []
for resource in DOMTree.getElementsByTagName("resources"):
  if ("os" in resource.attributes):
    if (resource.attributes["os"].value != platform.system()):
      continue
  nodes = resource.getElementsByTagName("jar")
  nodes += resource.getElementsByTagName("nativelib")
  for jar in nodes:
    file = jar.attributes["href"].value
    jars.append(file)
    if os.path.isfile(file):
      continue
    print("Downloading " + file)
    urllib.request.urlretrieve(codebase + file, file)

app = DOMTree.getElementsByTagName("application-desc")[0]
main = app.attributes["main-class"].value
args = []
for arg in app.getElementsByTagName("argument"):
  args.append(arg.firstChild.data)

cmd = "\"" + java_path + os.path.sep + "bin\\java\" "
# cmd = "java "
cmd += "-classpath " + os.pathsep.join(jars) + " "
cmd += main + " "
cmd += " ".join(args)

print("Running command:")
print(cmd)

subprocess.Popen(cmd)
