Excellent. This is where the real learning begins.

Most tutorials start by giving you a `.proto` file and saying "run this command." We're going to understand **why** each line exists.

# Lesson 2: Understanding `chat.proto`

Create the file:

```text
grpc-chat/
└── proto/
    └── chat.proto
```

---

# Step 1: The Simplest `chat.proto`

```proto
syntax = "proto3";

package chat;

message ChatMessage {
    string username = 1;
    string message = 2;
}

message ChatResponse {
    string reply = 1;
}

service ChatService {
    rpc SendMessage(ChatMessage) returns (ChatResponse);
}
```

Don't run anything yet. Let's understand every line.

---

# Line 1

```proto
syntax = "proto3";
```

This tells the Protocol Buffers compiler:

> "Use Protocol Buffers version 3."

There are two major versions:

- proto2
- proto3 ✅ (used in almost all new projects)

Always use `proto3` unless you're maintaining an older system.

---

# Line 2

```proto
package chat;
```

This is **not** a Python package.

It defines a namespace for your protobuf definitions.

Imagine two teams:

```
Team A

message User
```

```
Team B

message User
```

Without a package, there could be naming conflicts.

With packages:

```
chat.User
```

```
auth.User
```

They're different.

---

# What is a `message`?

A `message` is like a Python class.

Python:

```python
class ChatMessage:
    username: str
    message: str
```

Proto:

```proto
message ChatMessage {
    string username = 1;
    string message = 2;
}
```

When you compile the `.proto` file, gRPC generates an equivalent Python class for you.

---

# Why `= 1` and `= 2`?

This is one of the most important concepts.

```proto
string username = 1;
string message = 2;
```

These are **field numbers**, not default values or indexes.

Protocol Buffers don't send field names over the network. They send the field number.

Think of it like this:

| Field    | Number |
| -------- | ------ |
| username | 1      |
| message  | 2      |

Instead of sending:

```json
{
  "username": "Alice",
  "message": "Hello"
}
```

protobuf sends something conceptually closer to:

```
1 -> Alice

2 -> Hello
```

That's one reason protobuf is much smaller and faster than JSON.

---

# Why must field numbers never change?

Suppose version 1 is:

```proto
message ChatMessage {
    string username = 1;
    string message = 2;
}
```

A client sends:

```
1 = Alice

2 = Hello
```

Later you accidentally change:

```proto
message ChatMessage {
    string message = 1;
    string username = 2;
}
```

Now the server interprets:

```
Message = Alice

Username = Hello
```

Everything breaks.

**Rule: once a field number is published, never reuse or renumber it.**

---

# Why add new fields at the end?

Good:

```proto
message ChatMessage {
    string username = 1;
    string message = 2;
    string room = 3;
}
```

Bad:

```proto
message ChatMessage {
    string room = 1
    string username = 2
    string message = 3
}
```

Backward compatibility is a major design goal of Protocol Buffers.

---

# What is a `service`?

```proto
service ChatService
```

Think of a service as a Python class containing RPC methods.

Python analogy:

```python
class ChatService:

    def SendMessage(...):
        ...
```

The service groups related operations together.

---

# What is an RPC?

RPC stands for **Remote Procedure Call**.

Instead of calling a local function:

```python
reply = send_message(msg)
```

You're calling a function that runs on another machine.

You write:

```python
reply = stub.SendMessage(msg)
```

It _looks_ like a normal function call, but under the hood:

```
Client
   |
   | Serialize message
   |
Internet
   |
Server
   |
Run function
   |
Serialize response
   |
Client
```

gRPC handles all of that automatically.

---

# What does this line mean?

```proto
rpc SendMessage(ChatMessage) returns (ChatResponse);
```

Read it like English:

> The client sends a `ChatMessage`, and the server returns a `ChatResponse`.

This is a **Unary RPC**:

```
One request
↓

One response
```

Later we'll see:

### Server Streaming

```proto
rpc Subscribe(ChatRequest)
returns (stream ChatMessage);
```

```
One request

↓

Many responses
```

### Client Streaming

```proto
rpc Upload(stream ChatMessage)
returns (Result);
```

```
Many requests

↓

One response
```

### Bidirectional Streaming

```proto
rpc Chat(stream ChatMessage)
returns (stream ChatMessage);
```

```
Many requests

↓

Many responses
```

That's what we'll eventually use for our chat application.

---

# Our Data Model

For now, our chat is very simple.

```
Alice

↓

Hello

↓

Server

↓

Hello Alice!
```

The request needs:

- username
- message

The response only needs:

- reply

So our messages are:

```proto
message ChatMessage {
    string username = 1;
    string message = 2;
}

message ChatResponse {
    string reply = 1;
}
```

We'll add fields like `room`, `timestamp`, and `recipient` later.

---

# Assignment

1. Create `proto/chat.proto` with the contents above.
2. Read it line by line and make sure you understand the purpose of each part.
3. **Don't generate Python code yet.**

## In the next lesson, you'll learn:

- How `grpc_tools.protoc` generates Python code.
- What `chat_pb2.py` and `chat_pb2_grpc.py` contain.
- Why there are two generated files.
- How those files are used by both the client and the server.

Once you understand code generation, writing the server and client becomes much more intuitive.
