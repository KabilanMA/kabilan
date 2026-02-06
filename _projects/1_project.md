---
layout: page
title: TenSure
description: Sparse Tensor Compiler Fuzzer
img: assets/img/projects/tensure.png
importance: 1
category: Work
related_publications: true
---

TenSure {% cite tensure %} is a modular fuzzing framework designed to uncover correctness bugs in Sparse Tensor Compilers (STCs). It generates randomized sparse tensor kernels, executes them across compiler backends, and detects behavioral inconsistencies. TenSure is backend-agnostic and supports dynamic loading of multiple STC implementations.

More details can be found in the <a href="https://github.com/KabilanMA/TenSure">GitHub</a> repository.