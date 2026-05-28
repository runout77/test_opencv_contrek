#!/bin/bash

git clone --depth 1 --filter=blob:none --sparse https://github.com/runout77/contrek.git temp_repo
git -C temp_repo sparse-checkout set ext/cpp_polygon_finder/PolygonFinder
git -C temp_repo checkout
cp -r temp_repo/ext/cpp_polygon_finder/PolygonFinder/. contrek_core/
rm -rf temp_repo

mkdir build
cd build
cmake ..
make -j
