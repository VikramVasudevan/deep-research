from agents import Runner
from planner_agent import planner_agent, WebSearchPlan
from formatter_agent import formatter_agent
from openai.types.responses import ResponseTextDeltaEvent
from search_agent import search_agent
from reporting_agent import reporting_agent, ReportData
import asyncio

class ResearchManager:
    async def plan_searches(self, query:str):
        result = await Runner.run(planner_agent, f"Query: {query}")
        return result.final_output_as(WebSearchPlan)
    
    async def format_search_plan(self, search_plan: WebSearchPlan):
        result = Runner.run_streamed(formatter_agent, search_plan.model_dump_json())
        async for chunk in result.stream_events():
            if chunk.type == "raw_response_event" and isinstance(chunk.data, ResponseTextDeltaEvent):
                print(chunk.data.delta, end="", flush=True)
                yield chunk.data.delta

    async def search(self, search_term: str):
        result = await Runner.run(search_agent, search_term)
        return result.final_output_as(str)

    async def execute_search_plan(self, search_plan: WebSearchPlan):
       tasks = [self.search(search_term) for search_term in search_plan.searches]
       results = await asyncio.gather(*tasks)
       return results

    async def write_report(self, query:str, search_results:list[str]):
        result = await Runner.run(reporting_agent, f"Query: {query}\n\nSearch Results: {search_results}")
        return result.final_output_as(ReportData)