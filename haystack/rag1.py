# import necessary dependencies
from haystack import Pipeline, Document
from haystack.components.generators.chat import OpenAIChatGenerator
from haystack.components.retrievers import InMemoryBM25Retriever
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.builders import ChatPromptBuilder
from haystack.utils import Secret
from haystack.dataclasses import ChatMessage

# create a document store and write documents to it
document_store = InMemoryDocumentStore()
document_store.write_documents([
    Document(content="My name is Jean and I live in Paris."),
    Document(content="My name is Mark and I live in Berlin."),
    Document(content="My name is Giorgio and I live in Rome.")
])

# A prompt corresponds to an NLP task and contains instructions for the model. Here, the pipeline will go through each Document to figure out the answer.
prompt_template = [
    ChatMessage.from_system(
        """
        Given these documents, answer the question.
        Documents:
        {% for doc in documents %}
            {{ doc.content }}
        {% endfor %}
        Question:
        """
    ),
    ChatMessage.from_user(
        "{{question}}"
    ),
    ChatMessage.from_system("Answer:")
]

# create the components adding the necessary parameters
retriever = InMemoryBM25Retriever(document_store=document_store)
prompt_builder = ChatPromptBuilder(template=prompt_template, required_variables="*")
llm = OpenAIChatGenerator(api_key=Secret.from_env_var("OPENAI_API_KEY"), model="gpt-4o-mini")

# Create the pipeline and add the components to it. The order doesn't matter.
# At this stage, the Pipeline validates the components without running them yet.
rag_pipeline = Pipeline()
rag_pipeline.add_component("retriever", retriever)
rag_pipeline.add_component("prompt_builder", prompt_builder)
rag_pipeline.add_component("llm", llm)

# Arrange pipeline components in the order you need them. If a component has more than one inputs or outputs, indicate which input you want to connect to which output using the format ("component_name.output_name", "component_name, input_name").
rag_pipeline.connect("retriever", "prompt_builder.documents")
rag_pipeline.connect("prompt_builder", "llm")

# Run the pipeline by specifying the first component in the pipeline and passing its mandatory inputs. Optionally, you can pass inputs to other components.
question = "Who lives in Paris?"
results = rag_pipeline.run(
    {
        "retriever": {"query": question},
        "prompt_builder": {"question": question},
    }
)

print(results["llm"]["replies"])
