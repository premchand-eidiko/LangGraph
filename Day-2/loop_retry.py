import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from typing import TypedDict
from langgraph.graph import StateGraph,START,END

load_dotenv()

llm=ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.3
)

class State(TypedDict):
    question:str
    answer:str
    feedback:str
    is_valid:bool
    attempts:int

def generate_answer(state:State):
    attempt=state["attempts"]+1
    print(f"\nGenerating answer... Attempt {attempt}")    
    prompt = f"""
    You are a helpful AI assistant.
    User question: {state["question"]}
    Previous validator feedback:{state["feedback"]}
    Generate a clear, accurate and useful answer to the user's question.
    If previous feedback exists, improve the answer based on that feedback.
    """
    response=llm.invoke(prompt)
    return {
        "answer":response.content,
        "attempts":attempt
    }

def validate_answer(state: State):
    print("\nValidating answer...")
    prompt = f"""
    You are an answer quality validator.
    User question:{state["question"]}
    Generated answer:{state["answer"]}
    Evaluate whether the answer is:
    1. Relevant to the question
    2. Clear
    3. Factually reasonable
    4. Sufficiently detailed
    Respond in exactly this format:
    VALID: YES
    FEEDBACK: <short explanation>
    If the answer is good, say YES.
    If the answer needs improvement, say NO.
    """

    response = llm.invoke(prompt)
    validation = response.content.strip()
    print("\nValidator:")
    print(validation)

    if "VALID: YES" in validation.upper():
        return {
            "is_valid": True,
            "feedback": validation
        }
    else:
        return {
            "is_valid": False,
            "feedback": validation
        }

def route_after_validation(state:State):
    if state["is_valid"]:
        return "success"

    if state["attempts"]>=3:
        return "failed"

    return "retry"

def success(state:State):
    print(state["answer"])
    print(f"Completed in {state['attempts']} attempt(s).")
    return {}   

def failed(state:State):
    print("\nLast generated answer:")
    print(state["answer"])

    print("\nValidator feedback:")
    print(state["feedback"])   

    return {}          

graph=StateGraph(State)

graph.add_node("generate_answer",generate_answer)
graph.add_node("validate_answer",validate_answer)
graph.add_node("success",success)
graph.add_node("failed",failed)

graph.add_edge(START,"generate_answer")
graph.add_edge("generate_answer","validate_answer")
graph.add_conditional_edges(
        "validate_answer",
        route_after_validation,
            {
                "retry":"generate_answer",
                "success":"success",
                "failed":"failed"
            }
    )
graph.add_edge("success",END)
graph.add_edge("failed",END)

app=graph.compile()

question=input("\nEnter question: ")

result = app.invoke({
    "question": question,
    "answer": "",
    "feedback": "",
    "is_valid": False,
    "attempts": 0
})


print("\nFinal State:")
print(result)