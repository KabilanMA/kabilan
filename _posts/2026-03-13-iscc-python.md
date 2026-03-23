---
layout: post
title: Polyhedral Compilation Basics - Hands-on with ISLPy
date: 2026-03-20 06:01:00
description: A concise guide to understand the Integer Set Python Library.
tags: formatting code
categories: notes
thumbnail: assets/img/blogs/iscc_basic.png
giscus_comments: true
related_posts: false
toc:
  beginning: false

---
<p style="text-align: left;">
      <a href="../iscc-python/">Previous</a>      
</p>


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
# 1. Define the iteration space (Set)
nested_loop_space = isl.Set("{ [x,y] : 0 <= x < 5 and 0 <= y < 5 }")
print(f"Iteration Space: {nested_loop_space}")

# 2. Define the access relation (Map)
access_map = isl.Map("{ [x,y] -> [z] : z = 2*x - y }")
print(f"Access Map: {access_map}")
```

### Calculating Memory Footprints

To find the memory footprint, the exact array indices our loop will touch, we need to combine the iteration space with the access map. In `islpy`, we can apply a map to a set using the `.apply()` method.

```python
memory_footprint = nested_loop_space.apply(access_map)
print(f"Memory Footprint: {memory_footprint}")
# Output: { [z] : -4 <= z <= 8 }
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
loop_space = isl.Set("{ [i] : 1 <= i < 10 }")

# The realistic, bounded dependency graph
exact_dependencies = dependency_map.intersect_domain(loop_space)
```

### Scheduling and Code Generation

The most powerful feature of `islpy` is taking these mathematical models and gernating new optimized C code. Let's look at the __Loop Interchange__ schedule we designed previously, which swaps the inner and out loops to improve cache performance:

```{ [x,y] -> [t1, t2] : t2 = i and t1 = j }```

To generate code, ISL uses an Abstract Syntax Tree (AST) builder called `isl.AstBuilder`. Before generating the tree, we must bound our new schedule map to our iteration space, just like we did with dependencies.

```python
# 1. Define the original space and the new interchange schedule
original_space = isl.Set("{ [i,j] : 0 <= i < 10 and 0 <= j < 10 }")
interchange_schedule = isl.Map("{ [i, j] -> [t1, t2] : t2 = i and t1 = j }")

# 2. Bound the schedule to the specific loop iterations
bounded_schedule = interchange_schedule.intersect_domain(original_space)

# 3. Initialize the AST Builder (with an empty context for simple loops)
builder = isl.AstBuild.from_context(isl.Set("{ :}"))

# 4. Generate the AST Node from the bounded schedule
ast_node = builder.node_from_schedule_map(bounded_schedule)

# 5. Print the generated C code!
print(ast_node.to_C_str())
```

When you run this Python script, the AST builder outputs the newly structured C code, perfectly reflecting the swapped `i` and `j` loops based purely on our mathematical map.

### Conclusion

By moving from abstract mathematical syntax into `islpy`, we can programmatically analyze and rewrite software execution. We used `isl.Set` for iteration spaces, `isl.Map` for relations, `.apply()` for footprint analysis, and `isl.AstBuild` to generate optimized code. This pipeline is the exact mechanism that polyhedral compiler engines use to safely and effectively speed up complex software.

<p style="text-align: left;">
      <a href="../iscc-python/">Previous</a>      
</p>