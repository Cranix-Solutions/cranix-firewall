#
# Copyright (C) 2024 Peter Varkoly <pvarkoly@cephalix.eu> Nürnberg, Germany.  All rights reserved.
#
DESTDIR         = /
SYSTEMD         = $(DESTDIR)/usr/lib/systemd/system/
TOOLS           = $(DESTDIR)/usr/share/cranix/tools/firewall/
TEMPLATES       = $(DESTDIR)/usr/share/cranix/templates/firewall/
TOPACKAGE       = Makefile LICENSE README.md templates sbin tools bin
HERE            = $(shell pwd)
REPO            = ~/OSC/home:pvarkoly:CRANIX
PACKAGE         = cranix-firewall

install:
	mkdir -p $(SYSTEMD) $(TOOLS) $(TEMPLATES) $(DOCS) $(DESTDIR)/usr/bin/ $(DESTDIR)/usr/sbin/
	install -m 755 sbin/* $(DESTDIR)/usr/sbin/
	install -m 755 bin/* $(DESTDIR)/usr/bin/
	install -m 755 tools/* $(TOOLS)
	install -m 644 templates/*conf $(TEMPLATES)
	install -m 644 templates/cranix-firewall.service $(SYSTEMD)

dist:
	xterm -e git log --raw  &
	if [ -e $(PACKAGE) ] ;  then rm -rf $(PACKAGE) ; fi
	mkdir $(PACKAGE)
	for i in $(TOPACKAGE); do \
	    cp -rp $$i $(PACKAGE); \
	done
	find $(PACKAGE) -type f > files;
	tar jcpf $(PACKAGE).tar.bz2 -T files;
	rm files
	rm -rf $(PACKAGE)
	if [ -d $(REPO)/$(PACKAGE) ] ; then \
	   cd $(REPO)/$(PACKAGE); osc up; cd $(HERE);\
	   mv $(PACKAGE).tar.bz2 $(REPO)/$(PACKAGE); \
	   cd $(REPO)/$(PACKAGE); \
	   osc vc; \
	   osc ci -m "New Build Version"; \
	fi

