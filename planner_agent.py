from pydantic import BaseModel, Field
from agents import Agent


HOW_MANY_SEARCHES = 3

class WebSearchPlan(BaseModel):
    searches: list[str] = Field(description="A list of web searches to perform to best answer the query.")

planner_agent = Agent(
    name="PlannerAgent",
    instructions=f"You are a helpful research assistant. Given a query, come up with a set of web searches \
to perform to best answer the query. Output {HOW_MANY_SEARCHES} terms to query for. Give only the list as output, no other text.",
    model="gpt-4o-mini",
    output_type=WebSearchPlan,
)
