---
title: "Pipelines and Glue Systems"
author: "poga"
date: 2021-12-12
tags:
  - Programming
  - MLOps
  - glues
categories:
  - Notes
---

**Context**: Machine Learning Projects are mainly just a complex interdependent pipeline. We desperately need a better abstraction for them.

<!--more-->

## Hidden Complexity

Here's a simple rule I used to evaluate if a problem has a well-defined programmable abstraction: can I implement it with just one text file and a text editor?

- With [Infrastructure as Code](https://docs.microsoft.com/en-us/devops/deliver/what-is-infrastructure-as-code), I can set up a reasonably complex cloud-native infrastructure from zero.
- With a good framework, I can create a full-feature website rapidly and deploy it straight to the customer.

Pipelines are nowhere close to them.

It's not really about text files or editors. It's about the feedback loop and the speed of iteration.If I can get results with just a text file and an editor, I can usually get results fast enough to create a fast feedback loop.

[A good feedback loop is everything](https://martinfowler.com/articles/developer-effectiveness.html). It creates the [flow](https://en.wikipedia.org/wiki/Flow_(psychology)). You will be "in the zone" easier. It allows [Continuous Delivery](https://docs.microsoft.com/en-us/devops/deliver/what-is-continuous-delivery). The end result will be better. And everyone can be a little bit happier.

### Inputs/outputs are messy

In pipelines, the expected input format for each stage is often underdocumented. Stages often rely on different triggers to connect to each other, such as cronjobs or hooks.

### fake "Scalability"

Yes, it will be easier to scale each stage. But you also have to scale a distributed, stateful, highly-available system while scaling stages.

### Observability

We still don't have a good tool for pipeline-wide observability. Debugging asynchronous tasks across stages is still a PITA.

### Single-source-of-truth

Good DevOps relies on a single source of truth: the git repoistory.

When developing with git, I can `import` a module without worrying about the library's version, infra, and runtimes. However, every stage in a pipeline is an island, connected together with duct tapes and cronjobs. It's like collaborating on a project by sending copies with floppy disks and reviewing patches with spreadsheets.

---

## Rewritable Pipelines and NIH

People like to write software by themselves, especially those they shouldn't.

> ... I formulated a theory about what makes a good product type: <br />1. Initial integration time (and cost) needs to be low/near zero to get eval and close sale. <br />2. Low competition from open source. <br />3. Needs to avoid typical NIH zones where programmers might (often irrationally) want to build their own. - [@pervognsen](https://twitter.com/pervognsen/status/1473194196399902721)


People like to write complex software because it feels like an achievement. But the real achievement lies in [rewritable softwares](https://www.youtube.com/watch?v=agw-wlHGi0E): software that is hard to write but then easy to rewrite.

> The software is hard to write in that you spend years patiently writing code, experimenting with complicated ideas, and exploring the problem space. You wrestle with intricate problems, many of them dead-ends, and pull heroic all-night debugging sessions. Gradually though, you discover the essence of the problem you are solving and you eliminate the accidental complexity. The software then is really simple and easy to understand. The complex ideas are conspicuous in their absence. People can read the code, understand it, and write it again themselves. "Is that all there is to it?"

**Pipelines are easy to write**. We have so many [log](https://kafka.apache.org/) [streaming](https://pulsar.apache.org/en/) [messaging](https://www.rabbitmq.com/) [pub/sub](https://nats.io/) platforms for building pipelines.
**Pipelines are hard to rewrite**. There are many hidden pre/post-conditions between stages, hard-to-reason timing issues and race conditions, and layers of abstractions that left so much performance behind.

I want an abstraction for pipelines that make people think: ["Is that all? I could rewrite that in a weekend"](https://github.com/lukego/blog/issues/12).

## Pipelines are Glue Systems

In my opinion, pipelines are another good example of [Glue Systems](/tags/glues/). We try to hide complexity behind a "pipeline" so we can only focus on well-defined stages.

Glue system is [Accidental complexity](https://en.wikipedia.org/wiki/No_Silver_Bullet). Glue systems are the platform you locked yourself in without knowing it. And worse, you're also the only vendor supporting it. So, good luck.
