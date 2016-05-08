build/index.html: 2*/**/*.md 2*/**/*.alias
	./gen.py build/ 2*/**/*.md 2*/**/*.alias

all: build/index.html

open: build/index.html
	if [ "`which xdg-open`" ]; then xdg-open build/index.html; \
	elif [ "`which open`" ]; then open build/index.html; \
	fi
