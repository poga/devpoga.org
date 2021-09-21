---
title: "On Building Glue Systems"
author: "poga"
date: 2021-09-18
tags:
  - Essays
  - Programming
categories:
  - Essays
---

![](./glue.jpg)

I spent most of my life building glue systems.

Sometimes, I got to work on a deep, sparkling project. But most of the time, my work is about gluing things together.

<!--more-->

---

## Situated Programming

Researches on glue systems have a long history, although the problem usually lures hackers instead of academics.

[Rick Hickey](https://en.wikipedia.org/wiki/Rich_Hickey), the creator of the Clojure programming language, called it "situated programming." It's about those kinds of programs that sit in the world and entangle with the world.

> situate - "to put in or on a particular site or place."

[Marcel Weiher](https://twitter.com/mpweiher) thinks that it is the ["success condition"](https://blog.metaobject.com/2021/07/glue-code-is-success-condition.html) in software technology and believe our tools and linguistic mechanisms haven't caught up to deal with this kind of problem.

I agree with them. So instead of avoiding talk about the glue system, I want to draw more attention to the problem.

---

## Glue Systems are Distributed Systems

Since a glue system is about connecting many isolated pieces into a coordinated abomination, it's naturally a distributed system and inherits common problems from distributed systems: **availability** and **concurrency**.

The quality of peers(the things being glued) heavily impacts the availability of the glue. However, we usually expected a glue system have higher availability than most of its peers since the glue is the last thing we created after all the peers are ready. And you need to fix all the problems left, good or bad.

It's concurrent since it connects to many peers with different latency, performance characteristics, and availability. And the glue cannot be the bottleneck of the whole system.

---

## Why we dislike glues

Most of the glues we encountered are:

1. **messy**: There's usually no build system, or only an extremely fragile build system exists for the glue.
2. **lack of maintenance**: We only look at glues when there's a problem; usually, shit hits the fan problem. We look at them in anger and try to forget about it as soon as possible.

---

## Solutions?

![](./switches.webp)

Do you know what's gluing the internet together? These cheap, ignored black boxes usually are called switches. Personally I found [erlang](https://www.erlang.org/) and [elixir](https://elixir-lang.org/) have high potential in the domain of glue systems. They're naturally concurrent and provides high availability. In addition, they can be easily monitored and observed.

Or can [Raku](https://www.raku.org) inherit the (notorious) fame of Perl, the omnipresent glue language?

What's your solution on Glue Systems?

