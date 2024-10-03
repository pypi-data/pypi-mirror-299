import logging
from typing import Optional
from pydantic import Field
from dria_workflows import WorkflowBuilder, Operator, Edge, Peek, Size, Expression, ConditionBuilder, \
    GetAll, Workflow, Write, CustomTool, HttpRequestTool, LlamaParser


class SumTool(CustomTool):
    name: str = "calculator"
    description: str = "A tool sums integers"
    lfs: int = Field(0, description="Left hand side of sum")
    rhs: int = Field(0, description="Right hand side of sum")


def sum_workflow() -> Workflow:

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    builder = WorkflowBuilder()
    builder.add_custom_tool(SumTool())

    builder.generative_step(
        id="sum",
        prompt="What is 10932 + 20934?",
        operator=Operator.FUNCTION_CALLING_RAW,
        outputs=[Write.new("call")]
    )

    flow = [
        Edge(source="sum", target="_end")
    ]
    builder.flow(flow)
    builder.set_return_value("call")
    workflow = builder.build_to_dict()
    print(workflow)
    return workflow

if __name__ == "__main__":
    w = sum_workflow()


    print(w.save("sum.json"))

    inp = "<function=calculator>{{\"lfs\": 10932, \"rhs\": 20934}}</function>"
    parsed = LlamaParser().parse(inp)[0] # take the first call
    print(parsed.arguments.lfs + parsed.arguments.rhs)
