#/usr/bin/sh
# Build Mishkal Package
default: all
# Clean build files
clean:
	
backup: 
	
#create all files 
all: 

# Publish to github
publish:
	git push origin master 

date=$(shell date +'%y.%m.%d-%H:%M')
doc:
	epydoc -v --config epydoc.conf

#build
md2rst:
	pandoc -s -r markdown -w rst README.md -o README.rst
md2html:
	pandoc -s -r markdown -w html README.md -o README.html
	
wheel:
	sudo python setup.py bdist_wheel
wheel3:
	sudo python3 setup.py bdist_wheel
sdist:
	sudo python3 setup.py sdist
sdist2:
	sudo python setup.py sdist
upload:
	echo "use twine upload dist/semawal-0.1.tar.gz"
install:
	sudo python setup.py install
install3:
	sudo python3 setup.py install


test:
	cd tests; python3 test.py -f samples/link_test.csv
