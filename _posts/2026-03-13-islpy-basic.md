---
layout: post
title: Polyhedral Compilation Basics - Hands-on with ISLPy
date: 2026-03-22 06:01:00
description: A concise guide to understand the Integer Set Python Library.
tags: formatting code
categories: notes
thumbnail: assets/img/blogs/iscc_basic.png
giscus_comments: true
related_posts: false
toc:
  beginning: false

---
<div style="display: flex; justify-content: space-between;">
  <span><a href="../iscc-basic/">Previous</a></span>
  <span><a href="../islpy-validity/">Next</a></span>
</div>


### Introduction
---

In the previous article, we explored the text-based syntax of the Integer Set Library (ISL) to automatically model loops, memory accesses and schedules. 
While the theory is powerful, modern compiler framework (like LLVM's Polly) rely on programmatic bindings to automate these optimizations.
I hope this article will bridge the gap between theory and practice using `islpy`, the Python wrapper for ISL.
We will take the mathematical sets and relations we defined previously and turn them into executable Python scripts, ultimately using them to generate optimized C code automatically.

First, we need to install the import the library:

```bash
pip install islpy
```

```python
import islpy as isl
```

### Translating Sets and Relations to Python

In `islpy`, the text-based syntax we learned translates directly into Python objects.
- An Iteration Space is represented by the `isl.Set` object.
- Relations (like memory accesses or dependencies) are represented by the `isl.Map` object.

Let's recreate the 2D nested loop iteration space and an access map from our previous examples:

```python
# define the iteration space (Set)
nested_loop_space = isl.Set("{ [i,j] : 0 <= i < 5 and 0 <= j < 10 }")
print(f"Iteration Space: {nested_loop_space}")

# define the access relation (Map)
access_map = isl.Map("{ [i,j] -> [k] : k = 2*i - j }")
print(f"Access Map: {access_map}")
```

### Calculating Memory Footprints

To find the memory footprint, the exact array indices our loop will touch, we need to combine the iteration space with the access map. In `islpy`, we can apply a map to a set using the `.apply()` method.

```python
memory_footprint = nested_loop_space.apply(access_map)
print(f"Memory Footprint: {memory_footprint}")
# Output: { [k] : -9 <= k <= 8 }
```

This mathematically proves the minimum and maximum bounds of our array access without ever executing the actual C code.

### Bounding Data Dependencies

When we write a dependency relation like `{ [s] -> [t] : s = t - 1 }` (meaning the target iteration `t` relies on the source iteration `s`), that mathematical map technically extends to infinity. 
To make our dependency graph accurate for compiler optimization, we must bound them to our specific loop's execution reality.
We do this by intersecting the domain (the source side) of the map with our actual iteration space using `.intersect_domain()`.

```python
# The infinite flow dependency
dependency_map = isl.Map("{ [s] -> [t] : s = t - 1 }")

# The actual loop bounds
loop_space = isl.Set("{ [i] : 1 <= i < 6 }")

# The realistic, bounded dependency graph
exact_dependencies = dependency_map.intersect_domain(loop_space)
print(exact_dependencies)
# Output: { [s] -> [t = 1 + s] : 0 < s <= 5 }
```

### Scheduling and Code Generation

The most powerful feature of `islpy` is taking these mathematical models and gernating new optimized C code structure. Let's look at the __Loop Interchange__ schedule we designed previously, which swaps the inner and out loops to improve cache performance:

```{ [x,y] -> [t1, t2] : t2 = i and t1 = j }```

To generate code, ISL uses an Abstract Syntax Tree (AST) builder called `isl.AstBuilder`. Before generating the tree, we must bound our new schedule map to our iteration space, just like we did with dependencies.

```python
# Define the original space and the new interchange schedule
original_space = isl.Set("{ [i,j] : 0 <= i < 5 and 0 <= j < 10 }")
interchange_schedule = isl.Map("{ [i,j] -> [t1,t2] : t2 = i and t1 = j }")

# Bound the schedule to the specific loop iterations
bounded_schedule = interchange_schedule.intersect_domain(original_space)

# Initialize the AST Builder (with an empty context for simple loops)
builder = isl.AstBuild.from_context(isl.Set("{ :}"))

# Generate the AST Node from the bounded schedule
ast_node = builder.node_from_schedule_map(bounded_schedule)

# Print the generated C code!
print(ast_node.to_C_str())
```

When you run this Python script, the AST builder outputs the newly structured C code, perfectly reflecting the swapped `i` and `j` loops based purely on our mathematical map.

Output from `ast_node.to_C_str()`:

```c
for (int c0 = 0; c0 <= 9; c0 += 1)
  for (int c1 = 0; c1 <= 4; c1 += 1)
    (c1, c0);
```

Notice how the loop structure has been completely reordered. What were originally nested `i` and `j` loops are now swapped: `c1` (iterating over `i`) is the innermost loop and `c0` (iterating over `j`) is the outer loop. 
To apply a different transformation, simply define a new schedule map and repeat the process—ISL handles all the complexity of generating correct, optimized code automatically. 
The cache performance relies on how `(c1, c0)` maps to memory, but in most typical cases `"{ [i,j] -> [t1,t2] : t1=i and t2=j }"` would give better cache locality.

The output is not a standalone compilable C program, but rather a structured loop skeleton generated from the AST. In a real compiler workflow, you would embed this skeleton within your actual computation body (replacing `(c1, c0)` with your kernel code) to produce a complete, optimized program. 
This separation of concerns—where the polyhedral model handles loop structure and memory optimization independently from your actual computation—is what makes ISL-based compilers so powerful for automated performance tuning.

### Conclusion

By moving from abstract mathematical syntax into `islpy`, we can programmatically analyze and rewrite software execution. We used `isl.Set` for iteration spaces, `isl.Map` for relations, `.apply()` for footprint analysis, and `isl.AstBuild` to generate optimized code. 
This pipeline is the exact mechanism that polyhedral compiler engines use to safely and effectively speed up complex software.

<div style="display: flex; justify-content: space-between;">
  <span><a href="../iscc-basic/">Previous</a></span>
  <span><a href="../islpy-validity/">Next</a></span>
</div>