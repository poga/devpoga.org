---
title: "Revisiting Modern Data Stack"
author: "poga"
date: 2023-05-29
tags:
  - engineering
categories:
  - Blog
---

## TL;DR

> *"It’s hard to make predictions in the ever evolving data landscape, but I am not sure if we need a better Airflow. Building a better Airflow feels like trying to optimize writing code that shouldn’t have been written in the first place." -* [https://dagster.io/blog/rebundling-the-data-platform](https://dagster.io/blog/rebundling-the-data-platform)
>

---

## Growing Pain

### The Future of Data

[https://databased.pedramnavid.com/p/the-future-of-data](https://databased.pedramnavid.com/p/the-future-of-data)

> Data mesh is, in some ways, the admission of defeat in the face of complexity. The demands of teams are so complex that we must break apart the whole thing into smaller, more manageable chunks. Sales get their metric, and Marketing gets theirs. When someone asks why the numbers don’t match, we tell them that they don’t match because they are different.
>

### ****The Next Generation Of All-In-One Data Stacks****

[https://medium.com/coriers/the-next-generation-of-all-in-one-data-stacks-f46069ad10fd](https://medium.com/coriers/the-next-generation-of-all-in-one-data-stacks-f46069ad10fd)

> That’s one of the benefits of the “[modern data stack](https://seattledataguy.substack.com/p/the-baseline-datastack-going-beyond)’’. In theory it provided the ability for smaller companies to only pay for what they needed in terms of consumption and data infrastructure size. Meaning they didn’t need to sign a 7-figure contract for 5 years in order to test out a few ideas they might have.

That continues to work but in some cases it’s a lot of work to put all those pieces together. So we have a 2nd or possibly 3rd generation of all-in-one tools that have become popular. They often offer a price per consumption based model which allows teams that can’t afford a massive contract to consider using said solutions(not all the solutions I am currently looking at do so, such as Incorta). But most do.
>

### How Scale Kills Data Teams

[https://dataproducts.substack.com/p/how-scale-kills-data-teams](https://dataproducts.substack.com/p/how-scale-kills-data-teams)

> I disagree with all of these approaches. Moving fast is good. Data teams must create incentives for producers to care about how data is being used. Data governance must be iterative and applied at an appropriate level when and where it’s needed. The solution is surprisingly, painfully simple. **Better data communication.**
>

---

## Scale Up

### **Re-Engineering the Data Value Chain | Part 1**

[https://moderndata101.substack.com/p/re-engineering-the-data-value-chain](https://moderndata101.substack.com/p/re-engineering-the-data-value-chain)

> The Data-First stack is synonymous with a programmable data platform which encapsulates the low-level data infrastructure and enables data developers to shift from build mode to operate mode. DFS achieves this through infrastructure-as-code capabilities to create and deploy config files or new resources and decide how to provision, deploy, and manage them. Data developers could, therefore, declaratively control data pipelines through a single workload specification or single-point management.
>

👻 so far, data-first stack seems just re-inventing “bank python” [https://calpaterson.com/bank-python.html](https://calpaterson.com/bank-python.html)


### **An oral history of Bank Python(2021)**

[https://calpaterson.com/bank-python.html](https://calpaterson.com/bank-python.html)

> One of the slightly odd things about Minerva is that a lot of it is "data-first", rather than "code-first". This is odd because the majority of software engineering is the reverse. For example, in object oriented design the aim is to organise the program around "classes", which are coherent groupings of *behaviour* (ie: code), the data is often simply along for the ride. Writing programs with MnTable is different: you group the data into *tables* and then the code lives separately. These two lenses for organising computations are at the heart of the object relational impedance mismatch which has caused [such grief](https://calpaterson.com/activerecord.html). The force is out of balance: many more programmers can design decent object-oriented classes than can bring a set of tables into third normal form. This is a large part of the reason that that annoying impedance mismatch keeps coming up
>

### **The Feedback Loops in Data that Will Change SaaS Architecture (2021)**

[https://tomtunguz.com/data-feedback-loop/](https://tomtunguz.com/data-feedback-loop/)

>
>
> 1. The cloud data warehouse will become an increasingly central part of the SaaS stack, not just the data stack.
> 2. The architecture enables SaaS companies to reimagine the largest categories of software and rebuild them to challenge the incumbents.

### **The Data Engineer is dead, long live the (Data) Platform Engineer**

[https://robertsahlin.substack.com/p/the-data-engineer-is-dead-long-live](https://robertsahlin.substack.com/p/the-data-engineer-is-dead-long-live)

> A data platform engineer becomes more of an infra/software engineer and doesn’t build data pipelines or data models, but provide services, tooling, environments (development, test, production) and support to create a great user experience of a self-serve data platform used by the cross-functional teams. Different roles in the cross-functional team may require different services, tooling and support to enable them to develop, test and operationalize different data deliverables, ex;
>

### **Build vs Buy**

[https://hysterical.substack.com/p/build-vs-buy](https://hysterical.substack.com/p/build-vs-buy)

### ****Rebundling the Data Platform****

[https://dagster.io/blog/rebundling-the-data-platform](https://dagster.io/blog/rebundling-the-data-platform)

> *"It’s hard to make predictions in the ever evolving data landscape, but I am not sure if we need a better Airflow. Building a better Airflow feels like trying to optimize writing code that shouldn’t have been written in the first place."*
>

### ****Dagster and the Decade of Data Engineering****

[https://dagster.io/blog/decade-of-data-engineering](https://dagster.io/blog/decade-of-data-engineering)

> The legacy view of orchestration—that it is a system solely for the scheduling and ordering of tasks in production—is holding the ecosystem back as data teams are forced to expensively integrate an entire suite of tools to have basic data management capabilities.

We believe orchestration is a critical component of a new layer: the data control plane. The purpose of this control plane is to house and manage the asset graph.
>
