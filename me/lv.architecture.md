1. Identify the types of queries

Looking at your example CSV/table:

Query Type	Example
Aggregation / statistics	"How many deals are Closed Won?"
Simple filtering	"Who is the lead owner of Walmart deal?"
Semantic / fuzzy lookup	"Find deals related to LinkedIn outreach in March"
Text-based retrieval	"Show me the company with Manuel Lowery"

So you essentially have two broad types of operations:

Structured queries — SQL or pandas-style operations directly on the PostgreSQL table.

Semantic searches — Embedding lookups in Haystack Document Store (FAISS, Milvus, etc.) for questions that require “understanding” the deal context.

2. Define your tools

Each tool is a callable component the agent can pick. For production, you’d define at least two tools:

Tool	Purpose	Input	Output
SQLDealQueryTool	Run aggregation or filtering queries on PostgreSQL	User query or structured parameters	Result table or value
EmbeddingSearchTool	Semantic search in Haystack Document Store	User query	Top-k chunks (text)

Optional: For production, you can add more specialized tools like:

CRMDataFormatter → Convert raw results to nicely formatted text

DealSummarizer → Summarize multiple deal chunks

ExternalWebSearch → If agent needs outside info (you already have SerperDevWebSearch)

3. Agent architecture

High-level flow:

          ┌───────────────┐
User Query │   Agent      │
          └──────┬──────┘
                 │
      ┌──────────┴───────────┐
      │ LLM decides which tool│
      └──────────┬───────────┘
      ┌──────────┴───────────┐
      │        Tool           │
      │ ┌───────────────────┐│
      │ │SQLDealQueryTool    ││
      │ └───────────────────┘│
      │ ┌───────────────────┐│
      │ │EmbeddingSearchTool ││
      │ └───────────────────┘│
      └──────────┬───────────┘
                 │
        LLM formats final answer
                 │
                 ▼
             User receives


Key points:

The LLM is the “orchestrator” — it decides which tool to call based on the query.

Tools do all heavy lifting (SQL queries, embeddings search).

LLM can also do post-processing → format tables, summarize, or generate natural-language answers.