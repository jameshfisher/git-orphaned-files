PREFIX ?= /usr/local
BINPREFIX ?= "$(PREFIX)/bin"

install:
	@mkdir -p $(DESTDIR)$(BINPREFIX)
	@echo "installing bin to $(DESTDIR)$(BINPREFIX)"
	cp -f ./git-orphaned-files $(DESTDIR)$(BINPREFIX)

uninstall:
	rm -f $(DESTDIR)$(BINPREFIX)/git-orphaned-files

.PHONY: install uninstall
