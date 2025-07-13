from agents import Agent

formatter_agent = Agent(
    name="FormatterAgent",
    instructions="You are a helpful research assistant. Given a list of web searches, format them into a markdown report. Title this as Search Plan. Output only the markdown for the list of searches, no other text.",
    model="gpt-4o-mini",
    output_type=str,
)

