---
title: "Haxe and Programming for Many Machines"
author: "poga"
date: 2021-05-11
tags:
  - Programming
  - Essays
categories:
  - Essays
---

The title sounds obvious. We always program for a machine! A program won't run itself!

<!--more-->

---

## The "Machine" Machine

Our program runs on CPUs made out of sands. Fortunately, we don't need to think about sands. For most programmers, the lowest level we care is something called **"instruction set architecture"**: x86, ARM, RISC-V... etc.

The instruction set architecture(ISA) gives us freedom to express ourself with many, many languages. And they will run on many, many type of machines.

These sand machines are blazing fast, but also inflexible. If there's [issues](https://en.wikipedia.org/wiki/Spectre_(security_vulnerability)) in them, we're in a world of trouble. If we want to try out new ideas, they cost billions to build.

---

## The "Virtual" Machine

So modern languages start to **bring their own machine**. For flexibility, and iteration speed.

Python, Go, JavaScript, Java, Erlang, Lua, .Net, and many thousands of languages all have their own virtual machines. with their own trade-offs.

---

## Program for a machine

So, which machine we prefer?

We want **actor-based concurrency**? [BEAM](https://en.wikipedia.org/wiki/BEAM_(Erlang_virtual_machine)) is the best.

We want **light-weight and embeddability**? [Lua](https://www.lua.org/) is designed for it.

We want **state-of-the-art garbage collection**? Java is always solid, but also kind of boring.

---

## Program within the kernel

eBPF is a sandboxed virtual machine lives inside Linux Kernel. It's a revolutionary technology that can run sandboxed programs in the Linux kernel without changing kernel source code or loading kernel modules.

By making the Linux kernel programmable, infrastructure software can leverage existing layers, making them more intelligent and feature-rich without continuing to add additional layers of complexity to the system or compromising execution efficiency and safety.

---

## Program for many machines

[Haxe](https://haxe.org/) is a languages designed to [**compile to many different machines**](https://haxe.org/documentation/introduction/compiler-targets.html): JavaScript, .NET(C#), PHP, Lua, Java, Python, ...etc and also its own VM: [Hashlink](https://hashlink.haxe.org/).

With Haxe, we can freely explore different machines without the limitations from the machines' native programming language.

It's fun. You should try it.

---

## So?

So let's say I want to try out new hardward ideas, or new way of packaging.

What should I do?

Should I get a FPGA?

Can it help me to design the next [m1](https://en.wikipedia.org/wiki/Apple_M1)? or next chip for hyperscalers(a.k.a. clouds)?

TBH I'm probably never going to achieve that. But with software, I have the freedom to play with ideas.
