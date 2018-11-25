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

### Getting a compiler
If you arent using ubuntu 18, you'll need to add a recent compiler version,
as ubuntu 16 ships a very old compiler. Here's how you can do that. Go to a shell
and enter

```bash
wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | sudo apt-key add -
```

Then, depending on your version, type

```bash
sudo apt-add-repository "deb http://apt.llvm.org/<version>/ llvm-toolchain-<version>-6.0 main"
sudo apt-get update
sudo apt-get install -y clang-6.0
```

Matching the name of your version against the list in 
[LLVM Debian/Ubuntu nightly packages](https://apt.llvm.org/)
under the ubuntu section. For instance, if you are using ubuntu 16, you should
put `xenial` where `<version>` is in the above example.

then, to use these compilers by default, run
```bash
echo "export CXX=/usr/bin/clang++" >> ~/.bashrc
echo "export CC=/usr/bin/clang" >> ~/.bashrc
source ~/.bashrc
```

### Building the code
To build this code, go to the source directory and type

```bash
mkdir build
cd build
conan install ..
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
and clion should work as well.

You should use [cpplint](https://github.com/cpplint/cpplint.git) and
[scan build](https://clang-analyzer.llvm.org/scan-build.html) to make sure
that the style and the code is acceptable.


# Python

Install with install.sh (you may have to customize the installation directory)

Uninstall with uninstall.sh

Remove any generated .pyc files with clean.sh

