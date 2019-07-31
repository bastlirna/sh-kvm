# sh-kvm
JNLP launcher alternative to access the APC KVM in SH server housing.

Tested on Windows 7 32bit, Java 6 have to be supplied separately (SE 1.6.0_45 works for me). Improvements welcomed:)

## How-to
1) unpack to your favorite location
2) unpack Java 6 to the java6 folder
3) login to KVM web as usual, download the JNLP file and open it with kvm.cmd
4) enjoy :)

### *Side note* Unpacking Java

Java installer is done in 3 levels of packing. 

1) Get installer (e.g. `jre-6uXX-windows-i586.exe`) and unpack it
2) There is `core.zip`, unpack it into `java6` folder
3) Main JAR files are packed in the [Pack200](https://en.wikipedia.org/wiki/Pack200) format (see [stackoverflow](https://stackoverflow.com/a/14480193)), so run:

```
for /r %f in (*.pack) do "%JAVA_HOME%\bin\unpack200.exe" -r -q "%f" "%~pf%~nf.jar"
```

> Without the last step, you will probably end up with this error message:
> 
> ```
> Error occurred during initialization of VM
> java/lang/NoClassDefFoundError: java/lang/Object
> ```
