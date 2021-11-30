---
title: "Domain Modeling Made Functional"
author: "poga"
date: 2020-04-10
tags:
  - Programming
  - Domain Modeling
  - Software Engineering
  - Note
  - Reading
categories:
  - Notes
---

![](/post/2020-04-10_domain-modeling-made-functional/book.jpg)

Notes on the book [Domain Modeling Made Functional: Tackle Software Complexity with Domain-Driven Design and F#](https://www.amazon.com/Domain-Modeling-Made-Functional-Domain-Driven/dp/1680502549).

<!--more-->

## Understanding the domain

A developer's job is to solve a problem through software.

### define a shared model

* focus on business events and workflows rather than data structures
* partition the problem domain into smaller subdomains
* create a model of each subdomain in the solution
* develop a common language (known as the "Ubiquitous language") that is shared between everyone involved

### Business events

The value of the business is created in the process of transforming data.

### Bounded Contexts

We therefore need to create a distinction between a “problem space” and a “solution space,” and they must be treated as two different things. To build the solution we will create a model of the problem domain, extracting only the aspects of the domain that are relevant and then re-creating them in our solution space

### bounded contexts as autonomous software components

In general, an event used for communication between contexts will not be just a simple signal but will also contain all the data that the downstream components need to process the event.

#### trust boundaries and validation

The perimeter of a bounded context acts as a “trust boundary.” Anything inside the bounded context will be trusted and valid, while anything outside the bounded context will be untrusted and might be invalid.

The job of the output gate is different. Its job is to ensure that private information doesn’t leak out of the bounded context, both to avoid accidental coupling between contexts and for security reasons.

### Contracts between bounded contexts

* A Shared Kernel relationship is where two contexts share some common domain design, so the teams involved must collaborate.
* A Customer/Supplier or Consumer Driven Contract relationship is where the downstream context defines the contract that they want the upstream context to provide.
* A Conformist relationship is the opposite of consumer-driven. The downstream context accepts the contract provided by the upstream context and adapts its own domain model to match.
* Anti-Corruption Layer in DDD terminology, often abbreviated as “ACL.” In the diagram above, the “input gate” often plays the role of the ACL—it prevents the internal, pure domain model from being “corrupted” by knowledge of the outside world.

build a context map with relationships

### workflow within a bounded context

The input to a workflow is always the data associated with a command, and the output is always a set of events to communicate to other contexts.

avoid domain events within a bounded context

### code structure within a bounded context

use onion architecture ~= clean architecture

keep IO at the edges

---

## Understanding Types

represent a domain with ADTs

* AND types = product types = records
* OR types = SUM types = enums

### Domain modeling with types

Use type systems to capture the domain model accurately and can be read and understood by domain experts.

simple types + sum/product types + functions

functions = workflows

### Integrity and Consistency in the Domain

parse, don't validate https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/

lots of examples...

#### Capturing Business Rules in the Type System

ex.
```
type​ CustomerEmail = ​  | Unverified ​of​ EmailAddress ​  | Verified ​of​ VerifiedEmailAddress ​// different from normal EmailAddress​

type​ SendPasswordResetEmail = VerifiedEmailAddress -> ...
```

#### Making Illegal States Unrepresentable in Our Domain

#### Consistency

consistency = atomicity of persistence

Consistency between different context is hard, use eventual consistency:

* do nothing
* retry
* compensating action

only update one aggregation per transaction

#### Modeling Workflow as Pipelines

We’ll create a "pipeline" to represent the business process, which in turn will be built from a series of smaller "pipes." Each smaller pipe will do one transformation, and then we’ll glue the smaller pipes together to make a bigger pipeline. This style of programming is sometimes called “transformation-oriented programming.”

Following functional programming principles, we’ll ensure each step in the pipeline is designed to be stateless and without side effects, which means each step can be tested and understood independently. Once we have designed the pieces of the pipeline, we’ll just need to implement and assemble them.

* Command as input
* Sharing Common Structures Using Generics
* Combining Multiple Commands in One Type
* Modeling an Order as a Set of States https://blog.yoshuawuyts.com/state-machines/
* Adding New State Types as Requirements Change
* Modeling Each Step in the Workflow with Types
* Creating the Events to Return
* Documenting Effects with signature
* Composing the workflow from the steps

Long-running workflow: Sagas

### Implement the model

#### Understand functions

basic functional programming tutorial

#### Implementation: Composing a Pipelien

* Some functions have extra parameters that aren’t part of the data pipeline but are needed for the implementation—we called these "dependencies"
* We explicitly indicated “effects” such as error handling by using a wrapper type like Result in the function signatures. But that means that functions with effects in their output cannot be directly connected to functions that just have unwrapped plain data as their input.

#### Implementation: Working with Errors

Using the result type to make errors explicit. `bind` and `map`.

#### Serialization

persistence: state that outlives the process that created it
Serialization: the process of converting from a domain-specific representation to a representation that can be persisted easily.

#### Persistence

* Push persistence to the edge
* CQRS
* Bounded Contexts must own their data storage
