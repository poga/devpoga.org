---
title: "Guide to Serve Machine Learning Models in Production"
author: "poga"
date: 2020-02-17
tags:
  - Programming
  - Machine Learning
categories:
  - Essays
---

Here's a simple checklist for people who deploy machine learning models to production. Based on my personal experience.

<!--more-->

### Before deployment

- **Identify Bias**: Will the bias affect users? Discuss with the product team.
- **Performance Profile**: List your hardware requirements: CPU/GPU/RAM/DISK, sustaining usage or burst?
- **Model file size**: Avoid network congestion. Decide on push-based or pull-based deployment.
- **Continuous testing**: Test the model on real-world data. Check for over-fitting.

### Deploying

* Prepare for rollback.
* Use canary deployment if possible.

### After deployment

* **Log Collection**: collect log for debugging, remove personal information, sample if needed.
* **Error handling**: No model is perfect. Respond to user feedback, fast.
* **Emergency response**: Be prepare to fix the application with heuristic rules.
* **Observability**: Detect concept drift in the real world asap.
