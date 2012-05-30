DESTDIR=/
PROJECT=diamond
VERSION=0.2.0

all:
	@echo "make run      - Run Diamond from this directory"
	@echo "make watch    - Watch and continuously run tests"
	@echo "make test     - Run tests"
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

watch:
	watchr test.watchr

test:
	python test.py

sdist:
	python setup.py sdist --prune

bdist:
	python setup.py bdist --prune

install:
	python setup.py install --root $(DESTDIR)

buildrpm: sdist
	python setup.py bdist_rpm \
		--post-install=rpm/postinstall \
		--pre-uninstall=rpm/preuninstall \
		--install-script=rpm/install

builddeb: sdist
	mkdir -p build
	tar -C build -zxf dist/$(PROJECT)-$(VERSION).tar.gz
	(cd build/$(PROJECT)-$(VERSION) && debuild -us -uc)

tar: sdist

clean:
	python setup.py clean
	rm -rf dist build MANIFEST
	find . -name '*.pyc' -delete

cleanws:
	find . -name '*.py' -exec sed -i'' -e 's/[ \t]*$$//' {} \;

.PHONY: run watch test sdist bdist install buildrpm builddeb tar clean cleanws
