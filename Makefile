DESTDIR=/
PROJECT=diamond
VERSION=0.2.0

all:
	@echo "make source   - Create source package"
	@echo "make install  - Install on local system"
	@echo "make buildrpm - Generate a rpm package"
	@echo "make builddeb - Generate a deb package"
	@echo "make clean    - Get rid of scratch and byte files"

source:
	python setup.py sdist --prune

install:
	python setup.py install --root $(DESTDIR)

buildrpm: source
	python setup.py bdist_rpm \
		--post-install=rpm/postinstall \
		--pre-uninstall=rpm/preuninstall

builddeb: source
	mkdir -p build
	tar -C build -zxf dist/$(PROJECT)-$(VERSION).tar.gz
	(cd build/$(PROJECT)-$(VERSION) && debuild -us -uc)

clean:
	python setup.py clean
	rm -rf build MANIFEST
	find . -name '*.pyc' -delete

.PHONY: source install buildrpm builddeb clean
