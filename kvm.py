# https://docs.oracle.com/javase/tutorial/deployment/deploymentInDepth/jnlpFileSyntax.html

import argparse
import xml.dom.minidom
import os
import urllib.request
import subprocess
import platform
import zipfile

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
nativelibs = []

# scan for files
for resource in DOMTree.getElementsByTagName("resources"):
  if "os" in resource.attributes:
    if resource.attributes["os"].value != platform.system():
      continue
  for jar in resource.getElementsByTagName("jar"):
    jars.append(jar.attributes["href"].value)
  for nativelib in resource.getElementsByTagName("nativelib"):
    nativelibs.append(nativelib.attributes["href"].value)

# download files
for file in jars + nativelibs:
  if os.path.isfile(file):
    continue
  print("Downloading " + file)
  urllib.request.urlretrieve(codebase + file, file)
  if file in nativelibs:
    print("Extracting " + file)
    zip = zipfile.ZipFile(file)
    for zip_file in zip.infolist():
      if zip_file.filename[-4:] == ".dll":
        zip.extract(zip_file, "lib")
    zip.close()

# prepare app
app = DOMTree.getElementsByTagName("application-desc")[0]
main = app.attributes["main-class"].value
args = []
for arg in app.getElementsByTagName("argument"):
  args.append(arg.firstChild.data)

# start app
cmd = "\"" + java_path + os.path.sep + "bin\\java\" "
# cmd = "java "
cmd += "-Djava.library.path=lib "
cmd += "-classpath " + os.pathsep.join(jars) + " "
cmd += main + " "
cmd += " ".join(args)

print("Running command:")
print(cmd)

subprocess.Popen(cmd)
