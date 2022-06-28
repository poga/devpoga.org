---
title: "Zero Trust Network"
author: "poga"
date: 2020-04-09
tags:
  - Programming
  - Security
  - Networking
  - Note
  - Reading
categories:
  - Blog
---

![](/post/2020-04-09_zero-trust-network/book.jpg)

Notes on the book [Zero Trust Network](https://www.amazon.com/Zero-Trust-Networks-Building-Untrusted/dp/1491962194).

<!--more-->

## Zero Trust Fundamentals

Zero trust aims to solve the inherent problems in placing our trust in the network. Instead, it is possible to secure network communication and access so effectively that physical security of the transport layer can be reasonably disregarded. It goes without saying that this is a lofty goal. The good news is that we’ve got pretty good crypto these days, and given the right automation systems, this vision is actually attainable.

A zero trust network is built upon five fundamental assertions:

* The network is always assumed to be hostile.
* External and internal threats exist on the network at all times.
* Network locality is not sufficient for deciding trust in a network.
* Every device, user, and network flow is authenticated and authorized.
* Policies must be dynamic and calculated from as many sources of data as possible.

Traditional approach(**perimeter model**): break networks into zones, different level of trust by zone.

If we instead declare that network location has no value, VPN is suddenly rendered obsolete.

![](/post/2020-04-09_zero-trust-network/architecture.png)

### Zero Trust Control Plane

Requests for access to protected resources are first made through the control plane, where both the device and user must be authenticated and authorized.

Once the control plane has decided that the request will be allowed, it dynamically configures the data plane to accept traffic from that client (and that client only).

The zero trust model dictates that all hosts be treated as if they’re internet-facing. The networks they reside in must be considered compromised and hostile.

## Managing Trust
Trust management is the most important component of a zero trust network.

Define threat model. The Internet environment has a fairly well understood threat model. In general, we assume that the end-systems engaging in a protocol exchange have not themselves been compromised. By contrast, we assume that the attacker has nearly complete control of the communications channel over which the end-systems communicate.

### Zero trust needs

* Strong authentication (with mutual TLS)
* Authenticating Trust (with PKI and CA): All zero trust networks rely on PKI to prove identity throughout the network. As such, it acts as the bedrock of identity authentication for the majority of operations.
* Least Privilege
* Variable Trust: Instead of defining binary policy decisions assigned to specific actors in the network, a zero trust network will continuously monitor the actions of an actor on the network to update their trust score.
* Control Plane vs Data Plane

## Network Agents
network agent = user x device

A network agent as an ephemeral entity that is formed on demand to evaluate a policy. The data that is used to form an agent — user or device information — will typically be stored in persistent storage and queried to form an agent. When this data is queried, the union of the data at that point in time is what we call an agent.

No existing standards.

## Making Authorization Decisions

![](/post/2020-04-09_zero-trust-network/authorization.png)

* Enforcement: execute decisions made by the rest of the system
* Policy engine: compare request against policy
* Trust engine: risk analysis
* Data store: source of truth for the current and past state of the system

## Trusting User/Device/Application/Traffic...

examples...

## Realizing a Zero Trust Network

* All network flows MUST be authenticated before being processed.
* All network flows SHOULD be encrypted before being transmitted.
* Authentication and encryption MUST be performed by the endpoints in the network.
* All network flows MUST be enumerated so that access can be enforced by the system.
* The strongest authentication and encryption suites SHOULD be used within the network.
* Authentication SHOULD NOT relies on public PKI providers. Private PKI systems should be used instead.
* Devices SHOULD be regularly scanned, patched, and rotated.

### Rollout

* Use configuration management as a stepping stone
* Application Authentication and Authorization
* Authenticating Load Balancers and Proxies
* Relationship-Oriented Policy to simplify policy
* Policy Distribution

Zero trust proxies are application-level proxy servers which can be used to secure a zero trust network. Proxies are deployed as infrastructure to handle authentication, authorization, and encryption responsibilities.

## Adversarial View

* Identify Theft
* DDoS
* Endpoint Enumeration
* Untrusted Computing Platform
* Social Engineering
* Physical Coercion
* Invalidation
* Control Plane Security

## Papers

https://cloud.google.com/beyondcorp?hl=zh-tw#researchPapers

