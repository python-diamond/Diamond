DESTDIR=/
PROJECT=diamond
VERSION :=$(shell bash version.sh )
RELEASE :=$(shell ls -1 dist/*.noarch.rpm 2>/dev/null | wc -l )
HASH	:=$(shell git rev-parse HEAD )
DISTRO=precise

all:
	@echo "make run      - Run Diamond from this directory"
	@echo "make config   - Run a simple configuration CLI program"
	@echo "make watch    - Watch and continuously run tests"
	@echo "make test     - Run tests"
	@echo "make docs     - Build docs"
	@echo "make sdist    - Create source package"
	@echo "make bdist    - Create binary package"
	@echo "make pypi     - Update PyPI package"
	@echo "make install  - Install on local system"
	@echo "make develop  - Install on local system in development mode"
	@echo "make rpm      - Generate a rpm package"
	@echo "make deb      - Generate a deb package"
	@echo "make sdeb     - Generate a deb source package"
	@echo "make ebuild   - Generate a ebuild package"
	@echo "make tar      - Generate a tar ball"
	@echo "make clean    - Get rid of scratch and byte files"

run:
	./bin/diamond --configfile=conf/diamond.conf --foreground --log-stdout

config:
	./bin/diamond-setup --configfile=conf/diamond.conf

watch:
	watchr test.watchr

test:
	./test.py

docs: version
	./build_doc.py --configfile=conf/diamond.conf

sdist: version
	./setup.py sdist --prune

bdist: version
	./setup.py bdist --prune

bdist_wheel: version
	USE_SETUPTOOLS=1 ./setup.py bdist_wheel

install: version
	./setup.py install --root $(DESTDIR)

develop: version
	USE_SETUPTOOLS=1 ./setup.py develop

rpm: buildrpm

buildrpm: sdist
	./setup.py bdist_rpm \
		--release=`ls dist/*.noarch.rpm | wc -l` \
		--build-requires='python, python-configobj' \
		--requires='python, python-configobj'

deb: builddeb

sdeb: buildsourcedeb

builddeb: version 
	dch --newversion $(VERSION) --distribution unstable --force-distribution -b "Last Commit: $(shell git log -1 --pretty=format:'(%ai) %H %cn <%ce>')"
	dch --release  "new upstream"
	./setup.py sdist --prune
	mkdir -p build
	tar -C build -zxf dist/$(PROJECT)-$(VERSION).tar.gz
	(cd build/$(PROJECT)-$(VERSION) && debuild -us -uc -v$(VERSION))
	@echo "Package is at build/$(PROJECT)_$(VERSION)_all.deb"

buildsourcedeb: version 
	dch --newversion $(VERSION)~$(DISTRO) --distribution $(DISTRO) --force-distribution -b "Last Commit: $(shell git log -1 --pretty=format:'(%ai) %H %cn <%ce>')"
	dch --release  "new upstream"
	./setup.py sdist --prune
	mkdir -p build
	tar -C build -zxf dist/$(PROJECT)-$(VERSION).tar.gz
	(cd build/$(PROJECT)-$(VERSION) && debuild -S -sa -v$(VERSION))
	@echo "Source package is at build/$(PROJECT)_$(VERSION)~$(DISTRO)_source.changes"

ebuild: buildebuild

buildebuild: version
	cat gentoo/diamond.ebuild | sed "s/GIT_HASH/${HASH}/" >> gentoo/diamond-$(VERSION).ebuild
	@echo "ebuild is at gentoo/diamond-$(VERSION).ebuild"

tar: sdist

clean:
	./setup.py clean
	rm -rf dist build MANIFEST .tox *.log
	find . -name '*.pyc' -delete

version:
	./version.sh > version.txt

vertest: version 
	echo "${VERSION}"

reltest:
	echo "$(RELEASE)"

distrotest:
	echo ${DISTRO}

pypi: version sdist bdist_wheel
	twine upload -s dist/*

.PHONY: run watch config test docs sdist bdist bdist_wheel install rpm buildrpm deb sdeb builddeb buildsourcedeb ebuild buildebuild tar clean cleanws version reltest vertest distrotest pypi
