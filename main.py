from dotenv import load_dotenv
import asyncio
from research_manager import ResearchManager
import gradio as gr
from planner_agent import WebSearchPlan
from agents.tracing import trace

load_dotenv(override=True)


async def run(query: str):
    with trace("deep-research"):
        yield "Planning searches..."
        search_plan = await ResearchManager().plan_searches(query)
        yield "Formatting search plan..."
        search_plan_markdown = ""
        async for chunk in ResearchManager().format_search_plan(search_plan):
            search_plan_markdown += chunk
            yield search_plan_markdown

        yield "Executing search plan..."
        search_results = await ResearchManager().execute_search_plan(search_plan)
        yield "Writing report..."
        report = await ResearchManager().write_report(query, search_results)
        yield report.markdown_report


async def execute_search_plan(search_plan_str: str):
    search_plan = WebSearchPlan.model_validate_json(search_plan_str)
    results = await ResearchManager().execute_search_plan(search_plan)
    return "\n\n".join(results)


with gr.Blocks() as ui:
    gr.Markdown("# Deep Research")
    query_textbox = gr.Textbox(
        label="What topic would you like to research?",
        value="modern musical instruments",
        scale=2,
    )
    run_button = gr.Button("Research", variant="primary", scale=0)
    search_plan_markdown = gr.Markdown(label="Search Plan")
    run_button.click(
        lambda: gr.update(interactive=False), inputs=None, outputs=run_button
    ).then(fn=run, inputs=query_textbox, outputs=search_plan_markdown).then(
        lambda: gr.update(interactive=True), inputs=None, outputs=run_button
    )
    query_textbox.submit(
        lambda: gr.update(interactive=False), inputs=None, outputs=query_textbox
    ).then(fn=run, inputs=query_textbox, outputs=search_plan_markdown).then(
        lambda: gr.update(interactive=True), inputs=None, outputs=query_textbox
    )

    ui.launch(inbrowser=True)
