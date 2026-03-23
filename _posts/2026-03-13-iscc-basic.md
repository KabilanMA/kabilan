---
layout: post
title: Polyhedral Compilation Basics - iscc Syntax
date: 2026-03-14 06:01:00
description: A concise guide to understand the Integer Set Library (ISL) syntax, iscc.
tags: formatting code
categories: notes
thumbnail: assets/img/blogs/iscc_basic.png
giscus_comments: true
related_posts: false
toc:
  beginning: false

---
<p style="text-align: right;">
      <a href="../iscc-python/">Next</a>      
</p>

### Introduction
---

The Integer Set Library (ISL) provides a powerful framework for analyzing and optimizing loops in computer programs. At its core is `iscc`, a text-based syntax that allows us to represent complex loop structures as mathematical objects. By describing loop iterations, memory accesses, and data dependencies using sets and relations, compilers can reason about code in a precise way. This article introduces the fundamental concepts of `iscc`, demonstrating how it models loops, memory, dependencies, and execution order to enable advanced compiler optimizations.

### Sets

By defining the _iteration space_ of a loop as a mathematical set, we can analyze exactly when a piece of code executes.

In ISL, a basic Set represents a collection of integer points bounded by linear constraints. It is generally written in this format:

    `{ [variables] : conditions }`

If we have a standard C loop:
```c
for (int i = 0; i < 10; i++) {
    // loop body
}
```
The iteration variable is `i`. and the bounds dictate that `i` starts at 0 and stops before 10. In ISL syntax, the Set representing all the values of `i` during execution is written as:

`{ [i] : 0 <= i < 10 }`

Example 2:

```c
for (int i = 0; i < 10; i++) {
    for (int j = 0; j < i; j++) {
        // loop body
    }
}
```

`{ [i,j] : 0 <= i < 10 and 0 <= j < i }`

### Relations

While Sets define when a loop runs, Relations define what it accesses in memory, like reading from or writing to an array.
A relation acts as a mathematical map from a domain (our loop variables) to a range (an array index).
The syntax uses an arrow `->` to connect them:

`{ [domain_variables] -> [range_variables] : conditions }`

```c
for (int i = 0; i < 10; i++) {
    for (int j = 0; j < i; j++) {
        A[i + j] = 0; 
    }
}
```
We want to map the loop iterations [i,j] to the specific memory index they access. If we let `[k]` represent the 1D index array `A`, the relation mapping the iteration space to the accessed memory is:
`{ [i,j] -> [k] : k = i+j }`

In ISL, if we apply an access Relation to an iteration Set, the calculator outputs a new Set representing the accessed memory locations (Finds the loop's memory footprint).

Let's take a simpler 1D example:
- __Iteration Set__ (S): `{ [i] : 0 <= i < 10 }` (Loop from 0 to 9)
- __Access Relation__ (R): `{ [i] -> [k] : k = i+2 }` (Accessing `A[i+2]`)

When we apply `R` to `S` in the ISL calculator, it computes the range of `k`. Since `i` ranges from 0 to 9, `k` will range from 2 to 11. The resulting memory footprint Set is: 

`{ [k] : 2 <= k <= 11 }`

### Data Dependencies

Dependencies tell the compiler if it is safe to run loop iterations in parallel or if they can be reordered. If iteration B needs a value computed by iteration A, B depends on A. This is called __Flow Dependency__ (or Read-After-Write).

Let's look at a classic example:
```c
for (int i = 1; i < 10; i++) {
    A[i] = A[i-1] + 5;
}
```
Here, the iteration `i` writes to `A[i]`, but it first has to read from `A[i-1]`. This means the current iteration relies on the result calculated by the previous iteration.

In ISL, we represent these dependencies just like memory accesses: as __Relations__. But instead of mapping iterations to memory, a dependency relation maps a _source iteration_ (the one doing the writing) to a _target iteration_ (the one doing the reading).

If we use `[s]` to represent the source iteration and `[t]` to represent the target iteration that depends on it, i.e., the target iteration always happens exactly one step after its source iteration, we can write the ISL relation as follows:

`{[s] -> [t]: t=s+1}`

Which means target iteration `t` must wait for the source iteration `s` to finish. Because of this specific flow dependency, the compiler knows it cannot run all iterations of this loop at the same time in parallel. Every step strictly relies on the previous one being completed.

### Schedules

While __Sets__ define what executes, and __Dependencies__ define the rules of ordering, a schedule defines exactly when each iteration actually runs. It does this by mapping the iteration Set to a _time_ space.

Because a Schedule is just a mapping from one space (iteration) to another (time), we write it as an ISL Relation:

`{ [domain_variables] -> [time_dimensions] : conditions }`

Let's look at out simple 1D loop again:

```c
for (int i = 0; i < 10; i++) {
    // loop body
}
```
The most basic schedule is just the original execution order, where iteration `i` simply executes at time `i` (`t = i`). Which can be written in ISL relation as follows:

`{[i] -> [t]: t=i}`

Now, let's look at a classic compiler optimization that schedules allow us to do easily: __Loop Interchange__. This is often used to improve memory locality (cache performance) when accessing multi-dimensional arrays.

Imagine we have a standard 2D loop:
```c
for (int i = 0; i < 10; i++) {
    for (int j = 0; j < 10; j++>) {
        // loop body
    }
}
```
The original sequential schedule for this uses a 2D time vector `[t1, t2]`. It looks like this:

`{[i,j] -> [t1,t2]: t1=i and t2=j}`

Here, the outer loop variable `i` dictates the major time step `t1`, and the inner loop variable `j` dictates the minor time step `t2`.

If the compiler decides it would be faster to swap the order of these loops (running `j` on the outside and `i` on the inside), it doesn't need to write the C code immediately; it just changes the schedule relation.

`{[i,j] -> [t1,t2]: t2=i and t1=j}`

By setting `t1 = j` and `t2 = i`, we have effectively made `j` the outer loop (the major time step) and `i` the inner loop (the minor time step).

When advanced compilers optimize code, they use ISL to take the original iteration Set, calculate the Dependency Relations, and then mathematically search for a new Schedule Relation (like the loop interchange we just looked at).

The golden rule of these optimizations is that all new schedules are only valid if it respects the dependencies.

### Conclusion

By abstracting iteration spaces into Sets, memory accesses into Relations, and ordering constraints into Dependencies, we can mathematically reason about program behavior. This abstraction allows advanced compilers to explore a wide range of valid program transformations, such as loop interchange, by simply manipulating these mathematical objects. The ultimate goal is to find an optimal Schedule that preserves the program's correctness (by respecting all dependencies) while significantly improving performance.

<p style="text-align: right;">
      <a href="../iscc-python/">Next</a>      
</p>