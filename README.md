# SRV – The Seawolf Router for Video

SRV is a rewrite and redesign of
[SVR](https://github.com/ncsurobotics/svr), the seawolf video router.

## Navigation

1.  [Goals](#goals)
2.  [Design](#design)
    1.  [Language Choice](#language-choice) 1 [Options](#options) 1.
        [C](#c) 2. [C++](#c-1) 3. [Python](#python) 4. [Java](#java) 5.
        [Scala](#scala)
        2.  [Decision](#decision)

## Goals

Along with SVR’s goals of providing a server and client for realtime
passing of video streams between applications, SRV aims to be well
documented, correctly implemented, and platform independent. Furtherore,
SRV aims to be a more updated version of SVR, using the `OpenCV 2`
library over `OpenCV`.

## Design

In order to meet these goals, SRV has made a few design changes to SVR.
Major design changes include using Java and Scala over C for
portability, using Gradle over Make and CMake for the build tool, and
providing a wrapper process that yeilds when the server has started to
simplify scripts that depend on the server.

### Language Choice

#### Options

The options with which creating SRV would be feasible include any
language that openCV bindings are available for.

##### C

C is a tried and true language, and, with python, forms most of the
current code on the robot.

###### Advantages

C’s advantages include being able to talk naturally about low level
details, a single, simple way to code. Furthermore, C is [easily wrapped
by python,](http://swig.org/) and it is [taught in the courses CSC 116
and 216 at NCSU.](https://www.acs.ncsu.edu/php/coursecat/directory.php)

###### Disadvantages

C’s relatively low level of abstraction becomes a problem when projects
grow large. C also has a weak type system and a lot of undefined
behavior, which seems anachronistic compared to other languages, which
can gaurentee more. But the biggest problem we have encountered with C
isn’t the weak type system, the undefined behavior, or the lack of
abstraction, but the platform-dependance. While we endeavor to support
*any* unix system, the number of systems that are de facto supported has
dwindled from the original list of Mac, Linux, and BSD to just Ubuntu.

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
a boatload of documentation, [annotation
processors](https://docs.oracle.com/javase/7/docs/api/javax/annotation/processing/Processor.html)
for dsls, [excellent](https://www.jetbrains.com/idea/)
[tooling](https://gradle.org/), and, most importantly to us, is
available on every platform that hosts the JVM, which includes most of
the unixes. Finally, Java has the excellent tool javadoc for generated
documentation.

###### Disadvantages

Java’s interpretation of object oriented programming is at times as
rediculous as [pants oriented
clothing.](https://steve-yegge.blogspot.com/2006/03/execution-in-kingdom-of-nouns.html)
This leads Java to have what is in some cases a less advanced type
system than C, and what is certainly a less advanced type system than
C++. The reintroduction of null as a type system escape hatch, something
C++ introduced references and templates to avoid, and the removal of sum
types, both result in NullReferenceExceptions that would actually be
avoidable in C and C++.

On top of these annoyances, java is incredibly verbose. Compare hello
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

These failings, added together, make Java a frustrating language to use.

##### Scala

###### Advantages

Scala is to Java as C++ is to C. Scala provides more flexible types and
better gaurentees, while still being able to interoperate seamlessly
with Java. As a JVM language, Scala gets all of the myriad benifits of
Java: portability, the Gradle build system, a garbage collector, an [ide
par excellece](https://www.jetbrains.com/idea/), annotations processors,
and a [familiar documentation
style.](https://docs.scala-lang.org/style/scaladoc.html) What’s more,
Scala cuts down on the verbosity of Java and removes the *pants oriented
clothing* issue, helping users to define the problem in terms of itself
instead of in terms of objects.

On a less technical side of things, Scala is [the second most paid
programming
language](https://insights.stackoverflow.com/survey/2017#technology-top-paying-technologies-by-region),
making it an excellent addition to any programmer’s toolbox.

###### Disadvantages

While Scala keeps many of the advantages of Java, it does not keep one
of the larger ones: the mindshare. For all its flaws, Java is the
garbage collected Lingua Franca, being the major platform for Android
and being available on Linux, Windows, and some other unixes.
Optimistically for Scala, it is just an improved Java, and the language
won’t matter. Pessimistically, the lack of resources and familiarity
would be a hinderance.

#### Decision

Our primary need is a portable language, ruling out C and C++. Python is
too high level, leaving Java and Scala. Java and Scala are not mutually
exclusive: they [interoperate
well](http://www.codecommit.com/blog/java/interop-between-java-and-scala),
as they are basically two sides of the same coin (the JVM). Because it
is more modern, more forward-looking, and less painful to write, SRV
will lean towards Scala over Java, leaving the door open to switch
between them.
