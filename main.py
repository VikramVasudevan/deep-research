from json import load
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
import gradio as gr
import json

class SearchOutput(BaseModel):
    query: str
    result: str

class ValidatorOutput(BaseModel):
    searchOutput: SearchOutput
    is_valid: bool

def search_agent(query: str) -> SearchOutput | None:
    client = OpenAI()
    response = client.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": query}],
        response_format=SearchOutput,
    )
    return response.choices[0].message.parsed

def validate_search_results(search_results: str | SearchOutput | None) -> ValidatorOutput | None:
    client = OpenAI()
    if search_results is None:
        return None
    response = client.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": search_results.model_dump_json() if isinstance(search_results, SearchOutput) else search_results}],
        response_format=ValidatorOutput,
    )
    return response.choices[0].message.parsed

def render_gradio_interface():
    with gr.Blocks() as demo:
        gr.Markdown("# Deep Research")
        query = gr.Textbox(label="Query", value="What is the capital of France?")
        searchButton = gr.Button("Search")
        searchResults = gr.Textbox(label="Search Results")
        validateButton = gr.Button("Validate")
        validateResults = gr.Textbox(label="Validate Results")

        query.submit(fn=search_agent, inputs=query, outputs=searchResults)
        searchResults.change(fn=validate_search_results, inputs=searchResults, outputs=validateResults)
        searchButton.click(fn=search_agent, inputs=query, outputs=searchResults)
        validateButton.click(fn=validate_search_results, inputs=searchResults, outputs=validateResults)

        demo.launch()

def main():
    print("Hello from deep-research!")
    load_dotenv(override=True)
    render_gradio_interface()
    # search_results = search_agent("What is the capital of France?")
    # print(search_results)
    # isValid = validate_search_results(search_results)
    # print(isValid)


if __name__ == "__main__":
    main()
