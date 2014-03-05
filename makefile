# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>

SETUPFLAGS =  --install-layout deb

all:

install:
	./setup.py install --root $(DESTDIR) $(SETUPFLAGS)

.PHONY: clean
clean:
	$(RM) *.class *.jar
	$(RM) *.o *.out
	$(RM) *.orig
	$(RM) *.pyc *.pyo
	$(RM) -r _build
	$(RM) -r build
	$(RM) -r dist
	$(RM) -r *.egg-info
