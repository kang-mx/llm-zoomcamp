import os
from openai import OpenAI
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

provider = TracerProvider()
provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("llm-zoomcamp")

from starter import index
from rag_helper import RAGBase


class RAGTraced(RAGBase):
    def rag(self, query):
        with tracer.start_as_current_span("rag"):
            return super().rag(query)

    def search(self, query, num_results=5):
        with tracer.start_as_current_span("search"):
            return super().search(query, num_results=num_results)

    def llm(self, prompt):
        with tracer.start_as_current_span("llm"):
            return super().llm(prompt)

gemini_client = OpenAI(
    api_key=os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

traced_rag = RAGTraced(
    index=index,
    llm_client=gemini_client,
    model="gemini-2.5-flash"
)

if __name__ == "__main__":
    query = "How does the agentic loop keep calling the model until it stops?"
    answer = traced_rag.rag(query)
    print(answer)