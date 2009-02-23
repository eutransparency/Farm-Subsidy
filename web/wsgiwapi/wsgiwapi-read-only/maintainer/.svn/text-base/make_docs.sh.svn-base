#!/bin/sh

epydoc -o ../docs/epydoc --exclude unittests --exclude testsupport --no-private --name="WSGIWAPI" --parse-only -u "../index.html" -q ../wsgiwapi
rst2html --link-stylesheet --stylesheet=media/docs.css ../docs/introduction.rst ../docs/introduction.html
rst2html --link-stylesheet --stylesheet=media/docs.css ../docs/reference.rst ../docs/reference.html
