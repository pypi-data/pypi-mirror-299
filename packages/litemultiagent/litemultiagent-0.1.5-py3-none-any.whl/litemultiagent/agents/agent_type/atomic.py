from typing import List, Dict, Any, Type
from litemultiagent.agents.agent_class.base import BaseAgent
from litemultiagent.tools.registry import ToolRegistry


class AtomicAgent:
    def __init__(self, agent_name: str, agent_description: str, parameter_description: str,
                 tool_names: List[str], meta_data: Dict[str, Any],
                 agent_class: Type[BaseAgent]):
        tool_registry = ToolRegistry()
        available_tools = {}
        tools = []
        for tool_name in tool_names:
            available_tools[tool_name] = tool_registry.get_tool(tool_name).func
            tools.append(tool_registry.get_tool_description(tool_name))

        self.agent = agent_class(agent_name, agent_description, parameter_description,
                                 tools, available_tools, meta_data)

    def execute(self, task: str) -> str:
        return self.agent.send_prompt(task)

    def __getattr__(self, name):
        return getattr(self.agent, name)

    def __call__(self, task: str) -> str:
        return self.execute(task)