==============================
Seawolf Router for Video (SRV)
==============================

The SRV library is a replacement for SVR ~~written entirely
in python.~~ The goal was to simplify the code used for
Seawolf's video streaming.

SRV contains a number of video sources (either live camera streams or streams of video files) which it can then broadcast to client applications. SRV was designed
with realtime robotic applications in mind.

# C++
In order to optimize the code, some is being rewritten in c++. 

## Building
Building this code requires [conan](https://github.com/conan-io/conan), cmake,
make, and a recent c++ compiler. (GCC 4.8 and Clang 7, both available in ubuntu 18.10, should work.)
To build this code, go to the source directory and type

```bash
mkdir build
cd build
conan install .. --build=missing
cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=1 ..
cd ..
# The file `compile_commands.json` is optional and only useful if you are using an IDE.
ln -s build/compile_commands.json
cd build
make
make doc
```
now there should be documentation in the `build/doc/index.html` file, and
the executable `srv` at `build/srv`.


## Editing
To edit the code, either [cquery](https://github.com/cquery-project/cquery.git) 
(more stable) or [ccls](https://github.com/MaskRay/ccls.git) (faster) are reccommended,
which can both be used with emacs, vscode, or neovim. Because we use cmake, code blocks
should work as well.

# Python

Install with install.sh (you may have to customize the installation directory)

Uninstall with uninstall.sh

Remove any generated .pyc files with clean.sh
