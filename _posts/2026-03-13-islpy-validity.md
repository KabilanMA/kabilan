---
layout: post
title: Polyhedral Compilation Basics - Validating Schedules
date: 2026-03-29 06:01:00
description: A guide to mathematically verifying loop execution order using the ISL.
tags: formatting code
categories: notes
thumbnail: assets/img/blogs/iscc_basic.png
giscus_comments: true
related_posts: false
toc:
  beginning: false

---
<div style="display: flex; justify-content: space-between;">
  <span><a href="../islpy-basic/">Previous</a></span>
  <span><a href="../islpy-validity/">Next</a></span>
</div>

### Introduction
---

In the first two articles of this series, we learned how to model loops mathematically and generate optimized C code structure using Python (`islpy`).
We explored how changing a loop's __Schedule__ (like swapping an inner and outer loop) cna dramatically change the execution order to improve performance.
But this raises a critical question: _How does the compiler know if a new schedule is safe?_
If an optimization schedules a target iteration (which reads a value) to run _before_ its source iteration (which writes that value), the program will compute the wrong answer. This article explains how advanced compilers mathematically prove that a schedule is _legal_ by checking it against the program's data dependencies.

### The Golden Rule of Scheduling

The fundamental rule of polyhedral compilation is simple: **A schedule is only valid if it respects all data dependencies.** 
In terms of time, this means for every dependency where iteration `S` (Source) must happen before iteration `T` (Target), the scheduled time for `T` must be greater than or equal to the scheduled time for `S`. 

If we ever find a situation where $$Time(T) < Time(S)$$, the schedule is invalid.

### Mapping Dependencies into Time

To check this rule in `islpy`, we need to translate our dependencies from _iteration space_ into _time space_. Let's start by defining a simple loop with a strict flow dependency (where each iteration relies on the one right before it):

```python
import islpy as isl

# the iteration space (Loop from 1 to 9)
loop_space = isl.Set("{ [i] : 1 <= i < 10 }")

# the dependency (iteration 't' depends on 's' where s = t - 1)
dependency_map = isl.Map("{ [s] -> [t] : s = t - 1 }")

# bound the dependencies to our actual loop
exact_deps = dependency_map.intersect_domain(loop_space).intersect_range(loop_space)
print(f"Iteration Dependencies: {exact_deps}")
# output: { [s] -> [t] : s = t - 1 and 1 <= s <= 8 }
```


<div style="display: flex; justify-content: space-between;">
  <span><a href="../islpy-basic/">Previous</a></span>
  <span><a href="../islpy-validity/">Next</a></span>
</div>