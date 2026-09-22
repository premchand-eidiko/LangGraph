# LangGraph — Complete Learning & Revision Notes

> A beginner-friendly guide to understanding LangGraph concepts, workflows, routing, loops, retries, and reflection systems.

---

## 1. What is LangGraph?

LangGraph is a framework for building **stateful, graph-based workflows and AI agent systems**.

Instead of thinking only in terms of:

```text
Input → Step 1 → Step 2 → Output
```

LangGraph lets us build workflows with branching, loops, retries, decisions, and iterative improvement.

### Mental model

```text
                    ┌──────────────┐
                    │   Decision   │
                    └──────┬───────┘
                           │
                    ┌──────┴──────┐
                    ↓             ↓
                 Path A         Path B
                    ↓             ↓
                 Action         Action
                    └──────┬──────┘
                           ↓
                          END
```

Think of LangGraph as a **workflow engine**:

- **State** = information carried through the workflow
- **Node** = work that needs to be performed
- **Edge** = connection between pieces of work
- **Conditional edge** = decision about where to go next
- **Loop** = going back to an earlier node
- **END** = workflow completion

---

# 2. Chain vs Graph

## Chain

A chain generally follows a fixed sequence.

```text
Input
  ↓
Step A
  ↓
Step B
  ↓
Step C
  ↓
Output
```

## Graph

A graph allows the workflow to make decisions.

```text
                 ┌──→ Path A ──→ END
                 │
Input → Decision ┤
                 │
                 └──→ Path B ──→ END
```

| Concept | Chain | Graph |
|---|---|---|
| Flow | Mostly linear | Flexible |
| Branching | Limited | Natural |
| Loops | Not the main model | Supported |
| State | Can be passed | Central concept |
| Complex workflows | Harder | Easier |
| Agent workflows | Limited | Well suited |

> **Chain = sequence of steps**
>
> **Graph = connected workflow with decisions and loops**

---

# 3. State

State is the **shared information available to nodes while the graph executes**.

Think of state as a shared notebook.

```text
                 STATE
        ┌─────────────────────┐
        │ name                │
        │ question            │
        │ answer              │
        │ status              │
        │ attempts            │
        └─────────────────────┘
             ↑           ↓
           Node A      Node B
```

A node can:

1. Read information from state.
2. Perform work.
3. Return updates to state.

Example:

```python
state["name"]
```

A node can return:

```python
return {
    "answer": "Hello Prem"
}
```

The updated value becomes available to later nodes.

---

# 4. State Schema

A state schema defines **what information the graph is expected to maintain**.

A common approach is `TypedDict`.

```python
from typing import TypedDict

class State(TypedDict):
    name: str
    age: int
    status: str
```

### Mental model

```text
State Schema
     ↓
Defines structure
     ↓
Actual State
     ↓
Contains current data
```

---

# 5. TypedDict

`TypedDict` defines the expected structure of a dictionary.

```python
class State(TypedDict):
    name: str
    age: int
```

The actual state is still a normal dictionary:

```python
{
    "name": "Prem",
    "age": 25
}
```

### Important distinction

```text
TypedDict
   ↓
Blueprint / structure

Dictionary
   ↓
Actual data
```

`TypedDict` does not create the dictionary itself.

---

# 6. StateGraph

`StateGraph` is used to build the graph.

```python
from langgraph.graph import StateGraph

graph = StateGraph(State)
```

Think of it as a blank workflow where we define:

- Nodes
- Edges
- Routing
- Loops
- Start point
- End point

### Mental model

```text
State Schema
     ↓
StateGraph
     ↓
Add Nodes
     ↓
Add Edges
     ↓
Compile
     ↓
Run
```

---

# 7. Nodes

A node represents **one unit of work**.

Usually, a node is a Python function.

```python
def greet(state):
    return {
        "message": f"Hello {state['name']}"
    }
```

Then it is added:

```python
graph.add_node("greet", greet)
```

### Node mental model

```text
       State
         ↓
   ┌───────────┐
   │   Node    │
   │           │
   │ Do work   │
   └─────┬─────┘
         ↓
   State update
```

---

# 8. Edges

An edge determines **where execution goes next**.

```python
graph.add_edge("node_a", "node_b")
```

This means:

```text
node_a → node_b
```

A normal edge has a fixed destination.

---

# 9. START and END

```python
from langgraph.graph import START, END
```

`START` represents where execution begins:

```python
graph.add_edge(START, "first_node")
```

`END` represents where execution finishes:

```python
graph.add_edge("last_node", END)
```

```text
START
  ↓
Node
  ↓
Node
  ↓
END
```

---

# 10. Basic Graph Lifecycle

```text
Define State
     ↓
Create StateGraph
     ↓
Define Nodes
     ↓
Add Nodes
     ↓
Add Edges
     ↓
Compile
     ↓
Invoke / Run
     ↓
Final State
```

Example:

```python
graph = StateGraph(State)

graph.add_node("node_a", node_a)
graph.add_node("node_b", node_b)

graph.add_edge(START, "node_a")
graph.add_edge("node_a", "node_b")
graph.add_edge("node_b", END)

app = graph.compile()

result = app.invoke(initial_state)
```

---

# 11. Basic Complete Workflow

```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    name: str
    greeting: str
    response: str

def greeting_node(state: State):
    return {
        "greeting": f"Hello {state['name']}!"
    }

def response_node(state: State):
    return {
        "response": state["greeting"] + " Welcome to LangGraph!"
    }

graph = StateGraph(State)

graph.add_node("greeting", greeting_node)
graph.add_node("response", response_node)

graph.add_edge(START, "greeting")
graph.add_edge("greeting", "response")
graph.add_edge("response", END)

app = graph.compile()

result = app.invoke({
    "name": "Prem",
    "greeting": "",
    "response": ""
})

print(result)
```

Workflow:

```text
START
  ↓
greeting
  ↓
response
  ↓
END
```

---

# 12. Conditional Routing

A normal edge always goes to a fixed destination:

```python
graph.add_edge("A", "B")
```

A conditional edge can choose between destinations:

```python
graph.add_conditional_edges(
    "classifier",
    router
)
```

### Mental model

```text
                Classifier
                    ↓
                  Router
               ↙    ↓    ↘
             A       B      C
             ↓       ↓      ↓
            END     END    END
```

---

# 13. Classifier vs Router

### Classifier

Determines what something is.

```text
Question
   ↓
Classifier
   ↓
"math"
```

### Router

Determines where execution should go.

```text
"math"
   ↓
Router
   ↓
Calculator node
```

### Combined mental model

```text
User Question
      ↓
  Classifier
      ↓
   Decision
      ↓
    Router
   ↙      ↘
Math     General
 ↓          ↓
Calculator Search
```

---

# 14. `add_conditional_edges()`

Typical pattern:

```python
graph.add_conditional_edges(
    "source_node",
    router_function,
    {
        "route_a": "node_a",
        "route_b": "node_b"
    }
)
```

The router returns a route name:

```python
return "route_a"
```

Example:

```python
def route_question(state):
    if state["type"] == "math":
        return "calculator"

    return "general"
```

Then:

```python
graph.add_conditional_edges(
    "classify",
    route_question,
    {
        "calculator": "calculator",
        "general": "general"
    }
)
```

---

# 15. Conditional Routing — Job Application

### State

```python
class State(TypedDict):
    name: str
    role: str
    experience_yrs: int
    decision: str
```

### Workflow

```text
START
  ↓
Receive Application
  ↓
Screen Resume
  ↓
Router
 ↙     ↘
Selected Rejected
 ↓         ↓
Send      Send
Selection Rejection
 ↓         ↓
END       END
```

### Screening

```python
def screen_resume(state):
    if state["experience_yrs"] > 2:
        return {"decision": "Selected"}

    return {"decision": "Rejected"}
```

### Router

```python
def route_decision(state):
    if state["decision"] == "Selected":
        return "send_selected"

    return "send_rejected"
```

The `if` in `screen_resume()` determines data, while the router determines the graph path.

---

# 16. `if` Inside a Node vs Graph Routing

### `if` inside a node

```python
def process(state):
    if state["amount"] > 1000:
        message = "Large transaction"
    else:
        message = "Normal transaction"

    return {
        "message": message
    }
```

The graph path has not changed:

```text
process
   ↓
next_node
```

### Conditional graph routing

```python
graph.add_conditional_edges(
    "process",
    router,
    {
        "large": "large_transaction",
        "normal": "normal_transaction"
    }
)
```

Now the graph path changes:

```text
             process
                ↓
              router
             ↙      ↘
          large    normal
            ↓         ↓
          Node       Node
            ↓         ↓
           END       END
```

> **An `if` can change data. A conditional edge can change the workflow path.**

---

# 17. Banking Transaction Validator

### State

```python
class State(TypedDict):
    account_holder: str
    balance: float
    transaction_amount: float
    status: str
    message: str
```

### Workflow

```text
START
  ↓
Validate Transaction
  ↓
Router
  ├── Amount > Balance
  │       ↓
  │   Insufficient Funds
  │       ↓
  │      END
  │
  ├── Amount > 100000
  │       ↓
  │   Flag For Review
  │       ↓
  │      END
  │
  └── Otherwise
          ↓
      Process Transaction
          ↓
         END
```

### Router

```python
def route_transaction(state):
    if state["transaction_amount"] > state["balance"]:
        return "insufficient_funds"

    elif state["transaction_amount"] > 100000:
        return "flag_for_review"

    else:
        return "process_transaction"
```

Check insufficient funds first.

For:

```text
Balance = 100000
Transaction = 150000
```

the transaction is greater than both the balance and 100000. The first condition routes it to `insufficient_funds`.

---

# 18. Loops

A loop means the graph goes back to an earlier node and executes it again.

Normal workflow:

```text
A → B → C → END
```

Looping workflow:

```text
A → B
    ↓
    C
    ↓
    B
    ↓
    C
    ↓
    B
    ↓
   END
```

### Mental model

> **Loop = Should I execute this step again?**

> **Conditional routing = Which path should I take?**

---

# 19. Loop with Exit Condition

A loop needs an exit condition.

```text
START
  ↓
Process
  ↓
Check Condition
  ↓
 ┌───────────────┐
 │ Exit reached? │
 └───────┬───────┘
       ↙   ↘
     NO     YES
      ↓       ↓
   Process    END
      ↑
      └────────
```

The workflow repeats until the condition says to stop.

---

# 20. Simple Counter Loop

```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    count: int

def increment(state: State):
    count = state["count"] + 1
    print(f"Count: {count}")
    return {"count": count}

def check_count(state: State):
    if state["count"] >= 5:
        return "end"

    return "continue"

graph = StateGraph(State)

graph.add_node("increment", increment)

graph.add_edge(START, "increment")

graph.add_conditional_edges(
    "increment",
    check_count,
    {
        "continue": "increment",
        "end": END
    }
)

app = graph.compile()

result = app.invoke({
    "count": 0
})

print(result)
```

Execution:

```text
count = 0
   ↓
increment → 1
   ↓
check
   ↓
continue
   ↓
increment → 2
   ↓
check
   ↓
continue
   ↓
increment → 3
   ↓
check
   ↓
continue
   ↓
increment → 4
   ↓
check
   ↓
continue
   ↓
increment → 5
   ↓
check
   ↓
END
```

The loop is created by:

```python
"continue": "increment"
```

The exit is created by:

```python
"end": END
```

---

# 21. Loop Safety

A loop should have a reliable stopping mechanism.

Unsafe:

```text
A
↓
B
↓
A
↓
B
↓
A
↓
...
```

Safe:

```text
A
↓
B
↓
condition
↙       ↘
repeat   END
```

Common safety mechanisms:

- Maximum iterations
- Maximum retries
- Successful validation
- Quality threshold
- Timeout
- Explicit exit condition

### Mental model

```text
Loop
  +
Exit condition
  +
Safety limit
  =
Controlled workflow
```

---

# 22. Retry Mechanism

Retry is a common use of looping.

```text
Attempt
   ↓
Validate
   ↓
Success?
 ↙       ↘
YES       NO
 ↓         ↓
END      Retry
           ↓
        Attempt
```

Example:

```text
Generate Answer
      ↓
Validate Answer
      ↓
Valid?
 ↙       ↘
YES       NO
 ↓         ↓
END      Generate Again
            ↓
         Validate
```

---

# 23. Retry with Maximum Attempts

A retry workflow should normally have a maximum number of attempts.

```text
Generate
   ↓
Validate
   ↓
Valid?
 ↙       ↘
YES       NO
 ↓         ↓
END      attempts < 3?
          ↙       ↘
        YES        NO
         ↓          ↓
       Retry       END
         ↓
      Generate
```

Example:

```python
def route_after_validation(state):
    if state["is_valid"]:
        return "success"

    if state["attempts"] >= 3:
        return "failed"

    return "retry"
```

This prevents an infinite retry loop.

---

# 24. Reflection

Reflection means the system **examines its generated result**, identifies weaknesses, and improves it.

Basic pattern:

```text
Generate
   ↓
Reflect / Critique
   ↓
Good enough?
 ↙       ↘
YES       NO
 ↓         ↓
END      Improve
           ↓
        Reflect
```

### Three components

```text
Generator
   ↓
Reflector / Critic
   ↓
Improver
   ↓
Reflector / Critic
   ↓
...
```

---

# 25. Reflection Mental Model

```text
Write answer
     ↓
Review answer
     ↓
Find weaknesses
     ↓
Improve answer
     ↓
Review again
```

The same concept can be implemented as a graph loop.

---

# 26. Reflection State

```python
class State(TypedDict):
    question: str
    answer: str
    feedback: str
    iteration: int
    is_good: bool
```

| Field | Purpose |
|---|---|
| `question` | User's question |
| `answer` | Current generated answer |
| `feedback` | Reviewer's feedback |
| `iteration` | Number of iterations |
| `is_good` | Whether the answer is acceptable |

---

# 27. Reflection Workflow

```text
                  ┌──────────────────┐
                  │ Generate Answer  │
                  └────────┬─────────┘
                           ↓
                  ┌──────────────────┐
                  │ Reflect / Review │
                  └────────┬─────────┘
                           ↓
                    Is answer good?
                      ↙          ↘
                    YES           NO
                     ↓             ↓
                   END          Improve
                                   ↓
                                   └──────→ Reflect
```

---

# 28. Reflection Example

A generator creates:

```text
Answer 1
```

The reviewer checks:

```text
Accuracy
Relevance
Clarity
Completeness
Beginner-friendliness
```

Example feedback:

```text
GOOD: NO

FEEDBACK:
The explanation is correct but does not explain
the difference between nodes and edges clearly.
```

The improvement node receives:

```text
Current answer
+
Reviewer feedback
```

and creates:

```text
Improved Answer
```

The improved answer is reviewed again.

---

# 29. Reflection Router

```python
def route_after_reflection(state):
    if state["is_good"]:
        return "success"

    if state["iteration"] >= 3:
        return "success"

    return "improve"
```

Workflow:

```text
Reflection
    ↓
 ┌──┴───────────┐
 ↓              ↓
success       improve
 ↓              ↓
END          Reflection
```

The iteration limit prevents endless improvement.

---

# 30. Retry vs Reflection

## Retry

```text
Failed
  ↓
Try again
```

The main goal is to repeat the operation.

## Reflection

```text
Generate
   ↓
Analyze result
   ↓
Identify weaknesses
   ↓
Improve
```

### Memory trick

> **Retry = Try again**
>
> **Reflection = Think about what went wrong, then improve**

---

# 31. Complete Reflection Code Pattern

```python
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.3
)

class State(TypedDict):
    question: str
    answer: str
    feedback: str
    iteration: int
    is_good: bool

def generate_answer(state: State):
    iteration = state["iteration"] + 1

    prompt = f"""
You are a helpful AI assistant.

User question:
{state["question"]}

Previous reflection feedback:
{state["feedback"]}

Generate a clear, accurate and beginner-friendly answer.

If previous feedback is available, improve the answer
based on that feedback.

Do not mention the reflection process in your answer.
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "iteration": iteration
    }

def reflect_answer(state: State):
    prompt = f"""
You are an expert reviewer.

User question:
{state["question"]}

Generated answer:
{state["answer"]}

Review the answer based on:

1. Accuracy
2. Relevance
3. Clarity
4. Completeness
5. Beginner-friendliness

Respond exactly in this format:

GOOD: YES

FEEDBACK: <short explanation>

If the answer needs improvement:

GOOD: NO
"""

    response = llm.invoke(prompt)
    reflection = response.content.strip()

    if "GOOD: YES" in reflection.upper():
        return {
            "is_good": True,
            "feedback": reflection
        }

    return {
        "is_good": False,
        "feedback": reflection
    }

def route_after_reflection(state: State):
    if state["is_good"]:
        return "success"

    if state["iteration"] >= 3:
        return "success"

    return "improve"

def improve_answer(state: State):
    prompt = f"""
You are an expert AI assistant.

User question:
{state["question"]}

Current answer:
{state["answer"]}

Reviewer feedback:
{state["feedback"]}

Improve the answer using the reviewer's feedback.

Make the answer:
- Accurate
- Clear
- Relevant
- Beginner-friendly
- Complete

Return only the improved answer.
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content
    }

def success(state: State):
    print(state["answer"])
    print(f"Completed in {state['iteration']} iteration(s)")
    return {}

graph = StateGraph(State)

graph.add_node("generate_answer", generate_answer)
graph.add_node("reflect_answer", reflect_answer)
graph.add_node("improve_answer", improve_answer)
graph.add_node("success", success)

graph.add_edge(START, "generate_answer")
graph.add_edge("generate_answer", "reflect_answer")

graph.add_conditional_edges(
    "reflect_answer",
    route_after_reflection,
    {
        "improve": "improve_answer",
        "success": "success"
    }
)

graph.add_edge("improve_answer", "reflect_answer")
graph.add_edge("success", END)

app = graph.compile()

question = input("Enter your question: ")

result = app.invoke({
    "question": question,
    "answer": "",
    "feedback": "",
    "iteration": 0,
    "is_good": False
})

print(result)
```

---

# 32. Important Workflow Patterns

## Sequential

```text
A → B → C → END
```

Every step happens in order.

## Conditional Routing

```text
       A
       ↓
    Router
    ↙   ↘
   B     C
   ↓     ↓
  END   END
```

The workflow chooses a path.

## Loop

```text
A → B
    ↓
    A
```

Work repeats.

## Loop with Exit

```text
A → B
    ↓
 condition
 ↙       ↘
A        END
```

Repetition continues until a condition is satisfied.

## Retry

```text
Generate
   ↓
Validate
   ↓
Valid?
 ↙     ↘
NO      YES
↓        ↓
Retry    END
```

An unsuccessful operation is attempted again.

## Reflection

```text
Generate
   ↓
Reflect
   ↓
Good?
 ↙   ↘
NO    YES
↓      ↓
Improve END
  ↓
Reflect
```

Output is evaluated and improved.

---

# 33. The Most Important Mental Model

When designing a workflow, ask:

```text
1. What information does the workflow need?
                     ↓
                  STATE

2. What work needs to happen?
                     ↓
                   NODES

3. What happens next?
                     ↓
                  EDGES

4. Can the path change?
                     ↓
          CONDITIONAL EDGES

5. Can something repeat?
                     ↓
                   LOOP

6. When should it stop?
                     ↓
              EXIT CONDITION

7. What happens if something fails?
                     ↓
                  RETRY

8. Can the output be reviewed and improved?
                     ↓
                REFLECTION
```

---

# 34. Complete Concept Map

```text
                         LANGGRAPH
                             │
             ┌───────────────┴────────────────┐
             ↓                                ↓
           STATE                            GRAPH
             │                                │
     ┌───────┴────────┐              ┌────────┴────────┐
     ↓                ↓              ↓                 ↓
 State Schema       Data           Nodes             Edges
                                      │                 │
                                      │          ┌──────┴──────┐
                                      │          ↓             ↓
                                      │       Normal      Conditional
                                      │       Edge          Edge
                                      │                       │
                                      │                    Router
                                      │                       │
                                      │                 ┌─────┴─────┐
                                      │                 ↓           ↓
                                      │              Path A       Path B
                                      │
                                      └──────────────┐
                                                     ↓
                                                   Loops
                                                     │
                                          ┌──────────┴─────────┐
                                          ↓                    ↓
                                       Retry              Reflection
                                          │                    │
                                       Validate            Critique
                                          │                    ↓
                                       Retry              Improve
                                          │                    │
                                          └──────────┬─────────┘
                                                     ↓
                                                    END
```

---

# 35. Debugging Checklist

### State key names

If the state has:

```python
experience_yrs: int
```

use:

```python
state["experience_yrs"]
```

not:

```python
state["experience_years"]
```

A mismatch can cause `KeyError`.

### Router return values

If the router returns:

```python
return "selected"
```

the conditional mapping must contain:

```python
"selected": "some_node"
```

### Node names

Make sure the node is registered before routing to it:

```python
graph.add_node("process", process)
```

### START connection

```python
graph.add_edge(START, "first_node")
```

### END connection

A completed path should eventually reach:

```python
END
```

### Loop exit

Every loop should have a condition that can eventually terminate.

### Maximum iterations

For retry/reflection workflows:

```python
if state["iteration"] >= 3:
    return "success"
```

---

# 36. Practice Exercises

## Exercise 1 — Simple Workflow

Build:

```text
START
  ↓
receive_user
  ↓
create_message
  ↓
END
```

State:

```python
name: str
message: str
```

## Exercise 2 — Conditional Routing

Build a student result workflow:

```text
START
  ↓
check_marks
  ↓
router
 ↙      ↘
Pass    Fail
 ↓       ↓
END     END
```

State:

```python
student_name: str
marks: int
result: str
```

## Exercise 3 — Banking Transaction Validator

Build:

```text
START
  ↓
validate_transaction
  ↓
router
 ├── insufficient_funds
 ├── flag_for_review
 └── process_transaction
```

State:

```python
account_holder: str
balance: float
transaction_amount: float
status: str
message: str
```

Routing:

```text
amount > balance
        ↓
insufficient_funds

amount > 100000
        ↓
flag_for_review

otherwise
        ↓
process_transaction
```

## Exercise 4 — Loop with Exit Condition

Build a graph that increments a number until it reaches `5`.

State:

```python
count: int
```

Workflow:

```text
START
  ↓
increment
  ↓
check
 ↙   ↘
NO   YES
↓     ↓
increment END
```

## Exercise 5 — Retry Workflow

Build:

```text
Generate
   ↓
Validate
   ↓
Valid?
 ↙   ↘
NO    YES
↓      ↓
Retry  END
```

Add a maximum of 3 attempts.

## Exercise 6 — Reflection Workflow

Build:

```text
Generate Answer
       ↓
Reflect
       ↓
Good?
   ↙       ↘
 YES        NO
  ↓          ↓
 END       Improve
              ↓
           Reflect
```

State:

```python
question: str
answer: str
feedback: str
iteration: int
is_good: bool
```

---

# 37. Quick Revision

| Concept | Meaning |
|---|---|
| LangGraph | Framework for stateful graph-based workflows |
| State | Shared information carried through the graph |
| State Schema | Defines the structure of state |
| TypedDict | Defines expected dictionary structure |
| StateGraph | Builder used to create the graph |
| Node | Unit of work |
| Edge | Defines where execution goes next |
| START | Entry point |
| END | Completion point |
| Conditional Edge | Chooses the next path |
| Router | Decides which route to take |
| Loop | Repeats part of the workflow |
| Exit Condition | Determines when a loop stops |
| Retry | Repeats after an unsuccessful attempt |
| Reflection | Reviews and improves an output |

---

# 38. One-Line Memory Tricks

```text
State       → What information do I have?

Node        → What work should I do?

Edge        → Where do I go next?

Router      → Which path should I take?

Loop        → Should I do it again?

Exit        → When should I stop?

Retry       → Try again after failure.

Reflection  → Review, improve, and try again.

START       → Where the workflow begins.

END         → Where the workflow finishes.
```

---

# 39. Final Mental Model

```text
                         USER INPUT
                              ↓
                            STATE
                              ↓
                           NODE
                              ↓
                           EDGE
                              ↓
                         DECISION?
                        ↙         ↘
                     PATH A      PATH B
                       ↓           ↓
                     NODE        NODE
                       ↓           ↓
                       └─────┬─────┘
                             ↓
                         NEED REPEAT?
                         ↙          ↘
                       YES          NO
                        ↓            ↓
                      LOOP          END
                        ↓
                     VALIDATE
                        ↓
                   FAILED / GOOD
                    ↙        ↘
                 RETRY      SUCCESS
                    ↓          ↓
                 AGAIN        END

For AI systems:

Generate
   ↓
Reflect
   ↓
Improve
   ↓
Reflect
   ↓
Good enough
   ↓
END
```

## Core principle

> **LangGraph turns application logic into a stateful workflow where nodes perform work, edges control movement, routers make decisions, loops repeat work, and conditions determine when execution should stop.**
