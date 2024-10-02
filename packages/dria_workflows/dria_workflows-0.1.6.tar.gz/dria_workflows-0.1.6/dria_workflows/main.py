import logging
from typing import Optional
from pydantic import Field
from dria_workflows import WorkflowBuilder, Operator, Edge, Peek, Size, Expression, ConditionBuilder, \
    GetAll, Workflow, Push, CustomTool, HttpRequestTool


class SearchTool(CustomTool):
    name: str = "Search Tool"
    description: str = "A tool that performs searches"
    query: str = Field("...", description="The search query")
    lang: Optional[str] = Field(None, description="The language for the search")
    n_results: Optional[int] = Field(None, description="The number of results to return")

def fibonacci() -> Workflow:
    """Generate questions for a given context and backstory.

    Args:
        input_data (dict): The input data to be used in the workflow.
        max_time (int, optional): The maximum time to run the workflow. Defaults to 300.
        max_steps (int, optional): The maximum number of steps to run the workflow. Defaults to 30.
        max_tokens (int, optional): The maximum number of tokens to use in the workflow. Defaults to 750.

    Returns:
        dict: The generated questions.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    builder = WorkflowBuilder()
    st = SearchTool()
    builder.add_custom_tool(st)

    # Step A: QuestionGeneration
    builder.generative_step(
        id="fibonacci",
        prompt="Write fibonnaci sequence method with memoization in rust",
        operator=Operator.FUNCTION_CALLING,
        outputs=[Push.new("code")]
    )

    flow = [
        Edge(source="fibonacci", target="_end")
    ]
    builder.flow(flow)
    builder.set_return_value("code")
    workflow = builder.build()

    return workflow

if __name__ == "__main__":
    w = fibonacci()
    print(w.model_dump_json())