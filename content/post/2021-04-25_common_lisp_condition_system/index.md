---
title: "The Common Lisp Condition System"
author: "poga"
date: 2021-04-25
tags:
  - Lisp
  - Programming
  - Condition
  - Notes
categories:
  - Notes
---

## Foundation of the Condition System

### Dynamic Variables

A nested stack of environment variables. Defined with `defvar`, `declare special`, or `defparameter`.

> In Common Lisp, it is not necessary to instantiate or refer to any separate context object nor enclose the environment in an object, because contextual information is available by means of dynamic variables, which can be accessed and rebound as appropriate. New means of passing contextual information can be provided by defining new dynamic variables, and utilizing this new information channel does not require creating or altering any existing abstractions. While this mechanism could be considered to be a form of dependency injection, it does not require support from a language framework of any sort (such as Java EE’s CDI); rather, it is built into the standard language.

### Non-local transfers of control

* `TAGBODY` and `GO`
* `BLOCK` and `RETURN-FROM`, `RETURN`
* `CATCH` and `THROW`

### Lexical closures

Let over lambda:

```lisp
(defvar *counter*
  (let ((x 0))
    (lambda () (incf x) x))
  )
```

## Condition vs Hooks

> There is an analogy between condition types and hook kinds which we have constructed earlier. Instead of creating hook kinds, which are symbols, we define new condition types, which denote Lisp types . Operations on Lisp types are more complex, since Lisp types are an implementation of mathematical sets; therefore, operating on those allows for more complexity, compared to matching symbols by equality.

### Example: singalling between handler and signal

```lisp
(defun call-people ()
  (setf *csgo-launched-p* nil)
  (dolist (person *phonebook*)
    (catch :do-not-call
      (signal 'before-call :person person)
      (call-person person)))
)

(defun skip-non-csgo-people (condition)
  (let ((person (person condition)))
    (unless (member :csgo person)
      (format t ";; Nope, not calling ~A.~%" (first person))
      (throw :do-not-call nil)
    )
  ))

(handler-bind
  ((before-call #'ensure-csgo-launched)
   (before-call #'skip-non-csgo-people))
  (call-people))
```

* `error` = `signal` and `invoke-debugger`
* `unwind-protect` protects against transfer of control
* Clustering handlers together means that a handler does not “see” any handlers bound in the same handler-bind form—meaning that it cannot cause itself or its “neighbors” to become invoked.

### Example: Restarts

```lisp
(defvar *mark-safe-p* nil)
(defvar *front-door-locked-p* t)
(defvar *back-door-locked-p* t)

(restart-bind
  ((escape-through-front-door
    (lambda ()
      (format t ";; Escaping through the front door.~%")
      (setf *mark-safe-p* t))
    :test-function
      (lambda (condition) (declare (ignore condition)) (not *front-door-locked-p*)))
  )
...)
```

* `compute-restarts` includes system-defined restarts. You can filter them with:

```lisp
(defvar *toplevel-restarts* '())

(defun compute-relevant-restarts (&optional condition)
  (set-difference (compute-restarts condition) *toplevel-restarts*))
```

* usually we use `handler-case` and `restart-case`

### Condition reports

> Condition objects are printed in their unreadable form if the dynamic variable *print-escape* is bound to t. However, when that same variable is bound to nil, printing a restart objects causes its report function to be invoked.

* use `warn` to warn a handled condition and still invoke debugger if not.
* `assert` also creates conditions that allows programmer to retry an assert.

## Conclusion

> It can be said that the action of invoking the hooks is, in fact, the activity of seeking advice about how to handle a particular situation that is implemented by calling a series of relevant hook functions in order from most to least specific.

> the actual purpose (of the condition system) is to maximize the possibilities and means by which a body of code can be externally instructed, or advised, to treat situations encountered during its execution. The technical details, such as executing hooks, invoking choices, or even entering the debugger, are only means to achieving an ideological goal of having a system that seeks and utilizes advice supplied to it by any available means—be it via programmatically supplying a handler function, via interactively choosing and invoking one of the predefined restarts, or by resolving the situation manually by means of using a REPL inside an interactive Lisp debugger.

* The role of a binding operator is to modify the environment in which other forms are run.
* The case-like operators, on the other hand, follow a different programming idiom.
* The ideas behind algebraic effects are surprisingly similar to the ones by Common Lisp condition system: they separate the act of signaling a given situation in the program from the act of handling it, and they make it possible to provide a set of handlers for these situations dynamically, at the call site of that piece of code. Many parallels between the Common Lisp condition system and the system of algebraic effects have been drawn, but it seems that the two ideas have developed independently from one another.
* It is one of the few aspects of Lisp which have not yet been adopted by other languages which are nowadays considered mainstream.

## Condition system in practice

* Unit test libraries
* Web framework: sending result over the network
* GUI: interactive querying
* Generator

