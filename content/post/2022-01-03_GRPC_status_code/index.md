---
title: "gRPC status codes"
author: "poga"
date: "2022-01-03T00:56:00+08:00"
tags:
  - Programming
categories:
  - Blog
---

[gRPC](https://grpc.io) defined [18 status codes](https://github.com/grpc/grpc/blob/0e00c430827e81d61e1e7164ef04ca21ccbfaa77/include/grpcpp/impl/codegen/status_code_enum.h) for returning different types of errors.

I think they're a pretty good reference if you want to design clear error handling for API.

<!--more-->

## Status Codes

### OK = 0

Not an error; returned on success.

### CANCELLED = 1

The operation was cancelled (typically by the caller).

### UNKNOWN = 2

Unknown error. An example of where this error may be returned is if a Status value received from another address space belongs to an error-space that is not known in this address space. Also errors raised by APIs that do not return enough error information may be converted to this error.

### INVALID_ARGUMENT = 3,

Client specified an invalid argument. Note that this differs from
FAILED_PRECONDITION. INVALID_ARGUMENT indicates arguments that are
problematic regardless of the state of the system (e.g., a malformed file
name).

### DEADLINE_EXCEEDED = 4,

Deadline expired before operation could complete. For operations that
change the state of the system, this error may be returned even if the
operation has completed successfully. For example, a successful response
from a server could have been delayed long enough for the deadline to
expire.

### NOT_FOUND = 5,

Some requested entity (e.g., file or directory) was not found.

### ALREADY_EXISTS = 6,

Some entity that we attempted to create (e.g., file or directory) already
exists.

### PERMISSION_DENIED = 7,

The caller does not have permission to execute the specified operation.
PERMISSION_DENIED must not be used for rejections caused by exhausting
some resource (use RESOURCE_EXHAUSTED instead for those errors).
PERMISSION_DENIED must not be used if the caller can not be identified
(use UNAUTHENTICATED instead for those errors).

### UNAUTHENTICATED = 16,

The request does not have valid authentication credentials for the
operation.

### RESOURCE_EXHAUSTED = 8,

Some resource has been exhausted, perhaps a per-user quota, or perhaps the
entire file system is out of space.

### FAILED_PRECONDITION = 9,

Operation was rejected because the system is not in a state required for
the operation's execution. For example, directory to be deleted may be
non-empty, an rmdir operation is applied to a non-directory, etc.

A litmus test that may help a service implementor in deciding
between FAILED_PRECONDITION, ABORTED, and UNAVAILABLE:
1. Use UNAVAILABLE if the client can retry just the failing call.
2. Use ABORTED if the client should retry at a higher-level
     (e.g., restarting a read-modify-write sequence).
3. Use FAILED_PRECONDITION if the client should not retry until
     the system state has been explicitly fixed. E.g., if an "rmdir"
     fails because the directory is non-empty, FAILED_PRECONDITION
     should be returned since the client should not retry unless
     they have first fixed up the directory by deleting files from it.
4. Use FAILED_PRECONDITION if the client performs conditional
     REST Get/Update/Delete on a resource and the resource on the
     server does not match the condition. E.g., conflicting
     read-modify-write on the same resource.

### ABORTED = 10,

The operation was aborted, typically due to a concurrency issue like
sequencer check failures, transaction aborts, etc.

See litmus test above for deciding between FAILED_PRECONDITION, ABORTED,
and UNAVAILABLE.

### OUT_OF_RANGE = 11,

Operation was attempted past the valid range. E.g., seeking or reading
past end of file.

Unlike INVALID_ARGUMENT, this error indicates a problem that may be fixed
if the system state changes. For example, a 32-bit file system will
generate INVALID_ARGUMENT if asked to read at an offset that is not in the
range [0,2^32-1], but it will generate OUT_OF_RANGE if asked to read from
an offset past the current file size.

There is a fair bit of overlap between FAILED_PRECONDITION and
OUT_OF_RANGE. We recommend using OUT_OF_RANGE (the more specific error)
when it applies so that callers who are iterating through a space can
easily look for an OUT_OF_RANGE error to detect when they are done.

### UNIMPLEMENTED = 12,

Operation is not implemented or not supported/enabled in this service.

### INTERNAL = 13,

Internal errors. Means some invariants expected by underlying System has
been broken. If you see one of these errors, Something is very broken.

### UNAVAILABLE = 14,

The service is currently unavailable. This is a most likely a transient
condition and may be corrected by retrying with a backoff.

*warning* Although data MIGHT not have been transmitted when this
status occurs, there is NOT A GUARANTEE that the server has not seen
anything. So in general it is unsafe to retry on this status code
if the call is non-idempotent.

See litmus test above for deciding between FAILED_PRECONDITION, ABORTED,
and UNAVAILABLE.

### DATA_LOSS = 15,

Unrecoverable data loss or corruption.

