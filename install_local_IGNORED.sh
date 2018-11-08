#/bin/bash
dir=$(cd $(dirname $0); pwd)

packages="/Users/kenji/Library/Application Support/Sublime Text 3/Packages/"
dest="$packages/Codic_debug"
if [ ! -d "$dest" ]; then
	mkdir "$dest"
fi
cp "$dir"/* "$dest"
