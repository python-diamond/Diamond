# Copyright 1999-2010 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

EAPI=4

inherit python git-2

PYTHON_DEPEND="2:2.4"
RESTRICT_PYTHON_ABIS="3.*"

DESCRIPTION="Diamond is a python daemon that collects system metrics and publishes them to Graphite (and others)."
HOMEPAGE="https://github.com/BrightcoveOS/Diamond"
LICENSE="MIT"

KEYWORDS="amd64 x86"
SLOT="0"

IUSE="
    -test
    -mongo
    -mysql
    -snmp
    -redis
"

RDEPEND="
    dev-python/configobj
    dev-python/setproctitle
    test?  ( dev-python/mock )
    mongo? ( dev-python/pymongo )
    mysql? ( dev-python/mysql-python )
    snmp?  ( dev-python/pysnmp )
    redis? ( dev-python/redis-py )
"
DEPEND="
    ${RDEPEND}
"

EGIT_REPO_URI="https://github.com/BrightcoveOS/Diamond.git"
EGIT_COMMIT="GIT_HASH"

pkg_setup() {
	python_set_active_version 2
	python_pkg_setup
}

src_test() {
	make test || eerror "Make test failed. See above for details."
}

src_install() {
    default
    newinitd "${S}/gentoo/init.d" diamond
}

pkg_info() {
	"${ROOT}"/usr/bin/diamond --version
}
