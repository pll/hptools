"""
Package the ilolib HP ILO control library and commands
"""
try:
    from setuputils import setup
except:
    from distutils.core import setup

# check that everything is checked in
# No unregistered, un-ignored files
# no modified files

# get the version and build number
version = open("VERSION").readline().strip()
(major, minor) = version.split('.')

buildfile = open("BUILD", 'r')
build = int(buildfile.readline().strip())
buildfile.close()

# Update build number
build += 1
buildfile = open("BUILD", 'w')
buildfile.write(str(build) + "\n")
buildfile.close()

# check in the VERSION and BUILD files

setup(
    name = "ilolib",
    version = "%s_%d" % (version, build),
    description = "Library and CLI script to interact with an HP ILO 2",
    author = "Mark Lamourine",
    author_email = "mark.lamourine@redhat.com",
    url = "http://irish.lab.bos.redhat.com/cloudstack/ilolib/",
    package_dir = {'': 'src'},
    py_modules = ['ilolib', 'ilossh', 'ilourl'],
    scripts = ['src/ilocommand'],
    license="GPL",
    long_description=""
    )



