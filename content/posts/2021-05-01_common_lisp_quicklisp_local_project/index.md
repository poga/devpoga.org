---
title: "Common Lisp Local Project Development with Quicklisp"
author: "poga"
date: 2021-05-01
tags:
  - Lisp
  - Programming
  - Notes
categories:
  - Blog
---

Probably the cleanest way to do it:

```lisp
(pushnew (truename "/projects/app/") ql:*local-project-directories* )
(ql:register-local-projects)
(ql:quickload :app)
```

From [Use Quicklisp to load personal projects from arbitrary locations.](https://www.darkchestnut.com/2016/quicklisp-load-personal-projects-from-arbitrary-locations/)

---

Alternatively, you can create a symlink in `~/quicklisp/local-projects/`.
