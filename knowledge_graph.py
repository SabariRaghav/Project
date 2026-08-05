import streamlit as st
import os
from dotenv import load_dotenv

from neo4j import GraphDatabase
from langchain_groq import ChatGroq


# Load environment variables
load_dotenv()


# -----------------------------
# GROQ MODEL
# -----------------------------

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)


# -----------------------------
# NEO4J CONNECTION
# -----------------------------

uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")


driver = GraphDatabase.driver(
    uri,
    auth=(username,password)
)



# -----------------------------
# GUARDRAILS
# -----------------------------

blocked_words=[
    "hack",
    "hacking",
    "virus",
    "malware",
    "bomb",
    "drugs"
]

MAX_LENGTH=300



# -----------------------------
# CREATE KNOWLEDGE GRAPH DATA
# -----------------------------

def create_graph():

    query="""

    CREATE 
    (python:Technology {name:"Python"}),
    (langchain:Technology {name:"LangChain"}),
    (neo4j:Database {name:"Neo4j"}),
    (rag:Concept {name:"RAG"}),

    (python)-[:USED_FOR]->(langchain),
    (langchain)-[:WORKS_WITH]->(neo4j),
    (rag)-[:USES]->(neo4j)

    """

    with driver.session() as session:
        session.run(query)



# -----------------------------
# SEARCH KNOWLEDGE GRAPH
# -----------------------------

def search_graph(question):


    query="""

    MATCH (a)-[r]->(b)

    WHERE 
    toLower(a.name) CONTAINS toLower($question)
    OR
    toLower(b.name) CONTAINS toLower($question)

    RETURN 
    a.name AS source,
    type(r) AS relation,
    b.name AS target

    LIMIT 10

    """

    with driver.session() as session:

        result=session.run(
            query,
            question=question
        )


        data=[]

        for record in result:

            data.append(
                f"{record['source']} -- {record['relation']} --> {record['target']}"
            )


    return "\n".join(data)




# -----------------------------
# GENERATE ANSWER USING GRAPH
# -----------------------------

def generate_answer(question,context):


    prompt=f"""

You are a Knowledge Graph AI assistant.

Use only the given graph information.

Knowledge Graph:

{context}


Question:
{question}


Explain clearly.

"""


    response=llm.invoke(prompt)

    return response.content




# -----------------------------
# EVALUATION
# -----------------------------


def evaluate_response(question,answer):


    prompt=f"""

Evaluate this AI answer.

Question:
{question}


Answer:
{answer}


Give scores:

Correctness:
Relevance:
Completeness:

Overall Score:

Feedback:

"""


    result=llm.invoke(prompt)

    return result.content




# -----------------------------
# STREAMLIT UI
# -----------------------------


st.set_page_config(
    page_title="Knowledge Graph AI",
    page_icon="🧠"
)


st.title("🧠 Knowledge Graph RAG using Neo4j + Groq")


st.write(
"""
Ask questions from your Knowledge Graph.
"""
)



# Create graph button

if st.button("Create Knowledge Graph"):

    create_graph()

    st.success(
        "Knowledge Graph created successfully!"
    )



question=st.text_input(
    "Ask your question:"
)



if st.button("Generate"):


    if not question.strip():

        st.warning(
            "Enter a question"
        )


    elif len(question)>MAX_LENGTH:

        st.error(
            "Question too long"
        )


    elif any(word in question.lower() for word in blocked_words):

        st.error(
            "Unsafe question"
        )


    else:


        with st.spinner("Searching Knowledge Graph..."):


            graph_context=search_graph(question)


            if graph_context=="":
                graph_context="No related information found."


            answer=generate_answer(
                question,
                graph_context
            )


            evaluation=evaluate_response(
                question,
                answer
            )



        st.success(
            "Generated!"
        )


        st.subheader(
            "🕸️ Graph Context"
        )

        st.write(
            graph_context
        )


        st.divider()


        st.subheader(
            "🤖 AI Answer"
        )

        st.write(
            answer
        )


        st.divider()


        st.subheader(
            "📊 Evaluation"
        )

        st.write(
            evaluation
        )