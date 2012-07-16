DESTDIR=/
PROJECT=diamond
VERSION=0.2.0

all:
	@echo "make run      - Run Diamond from this directory"
	@echo "make config   - Run a simple configuration CLI program"
	@echo "make watch    - Watch and continuously run tests"
	@echo "make test     - Run tests"
	@echo "make docs     - Build docs"
	@echo "make sdist    - Create source package"
	@echo "make bdist    - Create binary package"
	@echo "make install  - Install on local system"
	@echo "make buildrpm - Generate a rpm package"
	@echo "make builddeb - Generate a deb package"
	@echo "make tar      - Generate a tar ball"
	@echo "make clean    - Get rid of scratch and byte files"
	@echo "make cleanws  - Strip trailing whitespaces from files"

run:
	./bin/diamond --configfile=conf/diamond.conf --foreground

config:
	./bin/diamond-setup --configfile=conf/diamond.conf

watch:
	watchr test.watchr

test:
	./test.py

docs:
	./build_doc.py --configfile=conf/diamond.conf

sdist:
	./setup.py sdist --prune

bdist:
	./setup.py bdist --prune

install:
	./setup.py install --root $(DESTDIR)

buildrpm: sdist
	./setup.py bdist_rpm \
		--post-install=rpm/postinstall \
		--pre-uninstall=rpm/preuninstall \
		--install-script=rpm/install \
		--release=`ls dist/*.noarch.rpm | wc -l`

builddeb: sdist
	mkdir -p build
	tar -C build -zxf dist/$(PROJECT)-$(VERSION).tar.gz
	(cd build/$(PROJECT)-$(VERSION) && debuild -us -uc)

tar: sdist

clean:
	./setup.py clean
	rm -rf dist build MANIFEST
	find . -name '*.pyc' -delete

cleanws:
	find . -name '*.py' -exec sed -i'' -e 's/[ \t]*$$//' {} \;

.PHONY: run watch config test docs sdist bdist install buildrpm builddeb tar clean cleanws
