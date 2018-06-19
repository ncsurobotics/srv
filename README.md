# SRV – The Seawolf Router for Video

SRV is a rewrite and redesign of
[SVR](https://github.com/ncsurobotics/svr), the seawolf video router.

## Navigation

1.  [Goals](#goals)
2.  [Design](#design)
    1.  [Language Choice](#language-choice)
        1.  [Options](#options)
            1.  [C](#c)
            2.  [C++](#c-1)
            3.  [Python](#python)
            4.  [Java](#java)
        2.  [Decision](#decision)
    2.  [Build Tool](#build-tool)
    3.  [Client](#client)
    4.  [Server](#server)
    5.  [Server Protocol](#server-protocol)
    6.  [Timeline](#timeline)

## Goals

Along with SVR’s goals of providing a server and client for realtime
passing of video streams between applications, SRV aims to be well
documented, correctly implemented, and platform independent. Furtherore,
SRV aims to be a more updated version of SVR, using the `OpenCV 3`
library over `OpenCV 2`. Finally, SRV will drop SVR’s responsibility of
reading from input streams. Instead of reading video streams from video
devices, SRV will simply route packets passed to it. An external program
will be needed to read from the raw video sources and pass them to the
router.

## Design

In order to meet these goals, SRV has made a few design changes to SVR.
Major design changes include using Java over C for portability, using a
JVM based build tool over Make and CMake for the build tool, and adding
a wrapper to handle the lifecycle of the server.

### Language Choice

#### Options

The options with which creating SRV would be feasible include any
language that openCV bindings are available for.

##### C

###### Advantages

C is a tried and true language, and, with python, forms most of the
current code on the robot. C’s advantages include being able to talk
naturally about low level details, a single, simple way to code.
Furthermore, C is [easily wrapped by python,](http://swig.org/) and it
is [taught in the courses CSC 116 and 216 at
NCSU.](https://www.acs.ncsu.edu/php/coursecat/directory.php)

###### Disadvantages

C’s relatively low level of abstraction becomes a problem when projects
grow large. C also has a weak type system and a lot of undefined
behavior, which seems anachronistic compared to other languages, which
can gaurentee more. But the biggest problem we have encountered with C
isn’t the weak type system, the undefined behavior, or the lack of
abstraction, but the platform-dependance. Whats worse, C’s [“stringly
typed”](http://wiki.c2.com/?StringlyTyped) macro system, with its
`#include`s and `#define`s, results in unresolvable naming conficts,
even on supported systems. With name shadowing and modules, modern
languages apart from C have fixed this problem. While we endeavor to
support *any* unix system, the number of systems that are de facto
supported has dwindled from the original list of Mac, Linux, and BSD to
just Ubuntu.

##### C++

###### Advantages

C++ shores up most of the difficulties with C: code is much easier to
organize around classes, C++ has a high ceiling for abstraction, and
undefined behavior is easier to avoid. The type system is much advanced,
offering classes, code generation for generics, polymorphism, type
interference, and anonymous functions. C++ is not just a step up from C
but an entity of its own; it is the most general programming language
one can think of, offering procedural, functional, and object-oriented
paradigms, and giving programmers the raw power to redefine the language
as they wish.

###### Disadvantages

C++ may fill a programmer’s toolkit to the brim, but it fails to solve
our one major problem with C. Just like in C, C++ libraries have
platform dependent headers, and often suffers from “works on my machine”
syndrome.

##### Python

###### Advantages

Platform specific no more, Python can work on any platform while still
giving the option of reaching into C. Python is also relativley terse,
and closely follows established paradigms, lending it the reputation of
being easy to use. If there is any one language that doesn’t scare off
newcomers, it’s python.

###### Disadvantages

Python is, for the lack of a better word, fudgy. While in some domains
it is the perfect fit, when it is used in the wrong ones, the
disadvantages grow apparent quickly. For instance, the lack of static
types removes a basic sanity check one gets in other languages. It is
easy to reason about and write a small python program, but a large,
monolithic beast of a python program can be very hard to follow. Also,
python makes it difficult to talk about low level details.

Along with these organizational problems, there are technical ones too.
Whereas in C++ and C it is easy to tell if something is a value, a
pointer, or a reference, these distinctions are hidden from the user in
python when one is using wrapper code for C functions.

A perfect microcosm of python’s imperfections is python’s lack of [tail
call elimination.](https://en.wikipedia.org/wiki/Tail_call) For
reference, tail call elimination is the optimization of omtimizing away
tail calls, an optimization strategy turned on by default in [most c and
c++
compilers](https://stackoverflow.com/questions/34125/which-if-any-c-compilers-do-tail-recursion-optimization).
Tail call elimination can lead to greater use of recursion and immutable
variables, which can help a programmer express some problems, such as
problems of parsing, more naturally. However, as [Guido van
Rossum](https://gvanrossum.github.io/), the (purportedly benevolent)
dictator for life of python commands, “There is only one way to do it.”
Because tail call elimination allows programmers to use recursion,
[Mr. Rossum banished the optimization from the
language](http://neopythonic.blogspot.com/2009/04/tail-recursion-elimination.html),
forcing users to use loops instead. While this may preserve some of
Python’s integrity, it perfectly demonstrates python’s inflexibility.

##### Java

###### Advantages

Java’s largest advantage is it’s mindshare. It is [taught at ncsu in
CSC 230.](https://www.acs.ncsu.edu/php/coursecat/directory.php) It’s not
hard to see why it has a large amount of users: its extremely strict
adherence to class-based object orientation, similarity to C, and QOL
improvments over C and C++ such as a garbage collector all make Java an
easy language to jump in to. But its mindshare is not its only
advantage. Java also has a strict, strong, and polymorphic type system,
a module system, a boatload of documentation, [annotation
processors](https://docs.oracle.com/javase/7/docs/api/javax/annotation/processing/Processor.html)
for dsls, [excellent](https://www.jetbrains.com/idea/)
[tooling](https://junit.org/junit4/), and, most importantly to us, is
available on every platform that hosts the JVM, which includes most of
the unixes. Finally, Java has the excellent tool Javadoc for generated
documentation.

###### Disadvantages

Java’s largest technical disadvantage is its inability to interoperate
with other languages. Whereas C code is easily wrapped by any scripting
language, Java mostly limits itself to the JVM, ruling out the option of
wrapping Java code with Python code. In the distant future,
[Graalvm](http://www.graalvm.org/) may fix this problem, but for now,
Java is isolated to the JVM.

Java is also a dull tool when it comes to expressing classes of objects
that must have both extensible behavior and structure, leading to
inflexible APIs. While it is easy to add behavior to a fixed set of
structures via the [visitor
pattern](https://en.wikipedia.org/wiki/Visitor_pattern), or to add a new
structure with a fixed set of behaviors via
[inheritance](https://en.wikipedia.org/wiki/Inheritance_\(object-oriented_programming\)),
without [open
multimethods](https://en.wikipedia.org/wiki/Multiple_dispatch) or
[typeclasses](https://en.wikipedia.org/wiki/Type_class), it is difficult
[but not
impossible](https://oleksandrmanzyuk.wordpress.com/2014/06/18/from-object-algebras-to-finally-tagless-interpreters-2/)
to make extensible types that can have both new operations and new types
added. This problem is especially salient in type heirarchies where the
[object algebra
approach](https://oleksandrmanzyuk.wordpress.com/2014/06/18/from-object-algebras-to-finally-tagless-interpreters-2/)
does not work.

Luckily, [through code generation,](http://www.multij.org/) open
multimethods can be emulated. It is not a part of standard Java, and it
doesn’t play nicely with generics, but it is better than nothing.

Apart from technical disadvantages, Java also has many language warts.
Java’s interpretation of object oriented programming is at times as
rediculous as [pants oriented
clothing.](https://steve-yegge.blogspot.com/2006/03/execution-in-kingdom-of-nouns.html)
This leads Java to have what is in some cases a less advanced type
system than C, and what is certainly a less advanced type system than
C++. The reintroduction of null as a type system escape hatch, something
C++ introduced references and templates to avoid, and the removal of sum
types, both result in NullReferenceExceptions that would actually be
avoidable in C and C++.

On top of these annoyances, Java is incredibly verbose. Compare hello
world in Java

``` java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello world!");
    }
}
```

to hello world in python

``` python
print("Hello world")
```

if you need any evidence.

These failings, added together, can make Java a frustrating language to
use.

#### Decision

Our primary need is a portable language, ruling out C and C++. Python is
too high level and dynamic, leaving Java. Because we will only be using
the program to serve simply formatted data, there should be no
inter-platform friction, rendering Java an excellent choice.

### Build tool

Using make, as SVR has done for its utilities, has caused problems in
the past. Although make is common to all unixes, make runs external
processes that may not be. While make can and [has been replaced with
CMake](https://github.com/jsalzbergedu/svr), and while CMake is
theoretically platform-neutral, the complexity of compiling a mixed C
and python library results in a platform specific build system
(i.e. calling external processes and using bash). Luckily, there are
alternatives, especially for anything written on the JVM. Java projects
can use the platform-independent Gradle build system. That being said,
Gradle can still call external commands, so we still must be careful. If
we need to build, for instance, python libraries, we should make sure to
separate those libraries into their own packages, and build them with an
appropriate build tool.

### Wrapper

Much like SVR, the SRV server runs in the background. However, unlike
SVR, SRV is started via a wrapper, so that once the wrapper exits, the
caller of the wrapper will know whether or not SRV has sucessfully
started. For instance:

``` bash
srv --request LifecycleGet
if [ "$?" = "0" ]
then
    echo "SRV server already started."
else
    echo "Starting SRV server"
    srv start
    if [ "$?" = "0" ]
    then
        echo "SRV has sucessfully started"
        echo "Initializing server"
        srv --request LifecycleStart
        echo "Server initialized."
    else
        echo "SRV failed to start"
    fi
fi
```

The actual logic, however, will be in a python wrapper to the wrapper
executable, `srv`. The library will transparently start the server if it
is not up, pushing the server lifecycle out of sight and out of mind.

### Client

The goal of the client is to provide an interface for accessing video
streams served by the server. Because the client is interface-centric,
the relevant information can be found under [Server
Protocol](#server-protocol).

### Server

The goal of the server is to serve video streams. It takes these streams
from raw sources, like video cameras, and break them up into frames,
which can be accessed individually by the client. Therefore, the server
takes requests related to serving video streams.

#### Server State

The server’s state is exposed to the wrapper and can be edited via the
wrapper.

##### Lifecycle

Lifecycle is the category of the server’s state concerning what stage
the server is in.

The `Lifecycle` family of requests can be used to look into and alter
the state of the Lifecycle.

###### Lifecycle States

The server state will be one of Uninitialized, Initialized, or Killed,
and
Users.

| Name          | Description                                                                                                                                 |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| Uninitialized | The server has been started but not initialized.                                                                                            |
| Initialized   | The server has been initialized and is ready to use.                                                                                        |
| Killed        | The server is in the process of shutting down.                                                                                              |
| Users         | The number of users the server has. Should be increased by one by a client when it is added, and decreased by one when that client is done. |

##### Source

Source is the category of the server’s state concerning opening and
closing sources.

The `Source` category of requests can be used to look into and alter the
sources.

###### Source State

Sorces are UDP sockets that the server routes. Sources are given a name
and a number id. There can be up to 256 sources open at a time. The
server keeps an associative list (hash table) of a number (stored as a
byte) plus a name (stored as a string). This list can be accessed
through the wrapper using the `SourceList` request, which will return a
JSON object.

Mock JSON object example:

``` javascript
{
  "sources": [
    {
      "id": 1,
      "name": "sourcename"
    },
    {
      "id": 2,
      "name": "othersourcename"
    }
  ]
}
```

The source state will consist of a 256 entry-long associative array. The
array entries will consist of two fields: an id and a name. The server
will always open a source at the lowest possible id number, and when a
source is killed, free that number for re-use.

### Server Protocol

SRV uses two basic protocols: UDP for broadcasting and routing video
streams, and TCP for requests and responses.

#### TCP Requests and Responses

TCP requests will be used to change and inspect the server’s state. For
instance, the wrapper may ask the server to open a
stream.

##### Requests

| Name           | Description                                                                          | Response         |
| -------------- | ------------------------------------------------------------------------------------ | ---------------- |
| LifecycleGet   | Get the current state of the lifecycle.                                              | LifecycleState   |
| LifecycleStart | Start allocating resources. Transition the server from uninitialized to initialized. | LifecycleStarted |
| LifecycleKill  | Kill the server                                                                      | None             |

##### Responses

| Name             | Description                                                                    |
| ---------------- | ------------------------------------------------------------------------------ |
| LifecycleState   | The state of the lifecycle as a JSON object.                                   |
| LifecycleStarted | A JSON object containing a “error” field that is True when there was an error, |

#### UDP Data Routing

UDP will be used to broadcast video streams to all the client. The UDP
packets will be very simple: Firstly, they will be based on [capn
proto](https://capnproto.org/) for (de)cerealization\[1\]. The packets
start with one byte that serves as a relative time stamp, then have one
byte that determines which stream it is, then have a byte signalling if
the source has been closed, then the image data.

The byte that serves as a relative time stamp will be a number, 0-255,
that determines what relative position in the stream an image is. For
instance, the first image sent by the SRV server will be numbered 0,
then the next one will be 1, all the way up to 255. After 255, the next
number is 0.

The byte that determines which stream it is will be a number, 0-255,
which serves as the id of the stream. The id will be passed to the
server by the wrapper. The id will also be associated with a string
name, which is passed to the server by the wrapper. The server will then
hold that id, keeping it associated with the name. The ids then can be
queried through the wrapper process.

## Timeline

| Feature                   | Completed | Expected Date |
| ------------------------- | --------- | ------------- |
| SrvRequests               | Yes       | N/A           |
| SrvResponses              | No        | 07/01/18      |
| SrvWrapper                | No        | 06/24/18      |
| Srv (server)              | No        | 07/29/18      |
| Numpy array to udp script | No        | 08/05/18      |
| Python Wrapper Code       | No        | 08/12/18      |

1.  Spelling intentional.
