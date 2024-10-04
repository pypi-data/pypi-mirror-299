"""DAG definition and node implementations."""
import logging
import yaml
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from typing import Dict, Any, Type, Callable
from abc import ABC, abstractmethod
from sqlalchemy import create_engine
from .llm_providers import openai_call

log: logging.Logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

"""Node definitions."""


class Node(ABC):
    def __init__(
        self,
        config: Dict[str, Any],
        secrets: Dict[str, str],
        custom_functions: Dict[str, Callable] = None,
    ):
        self.config = config
        self.secrets = secrets
        self.functions = {}
        if custom_functions:
            self.functions.update(custom_functions)

    @abstractmethod
    def execute(self, input_data: Any) -> Any:
        """
        Execute the node's operation.

        :param input_data: The input data for this node, typically the output from the previous node.
        :return: The result of this node's operation.
        """
        pass

    @abstractmethod
    def validate_config(self) -> bool:
        """
        Validate that the node's configuration is correct and complete.

        :return: True if the configuration is valid, False otherwise.
        """
        pass


class CSVNode(Node):
    """Node to read a CSV file."""

    def execute(self, input_data: Any) -> Any:
        return pd.read_csv(self.config["path"])

    def validate_config(self) -> bool:
        return "path" in self.config


class SQLNode(Node):
    """Node to execute a SQL query."""

    def execute(self, input_data: Any) -> Any:
        if not self.validate_config():
            raise ValueError("Invalid SQL node configuration.")
        connection_string = f"postgresql://{self.secrets['db_user']}:{self.secrets['db_password']}@{self.secrets['db_host']}/{self.secrets['db_name']}"
        return read_sql(self.config["query"], connection_string)

    def validate_config(self) -> bool:
        return "query" in self.config and "database_url" in self.secrets


class LLMNode(Node):
    """Node to query an LLM API with a template. If given a string, it
    will fill in the template and return the result. If given a DataFrame,
    it will turn the `input_column` into a list of strings, fill in the
    template for each string, and return a list of results."""

    def execute(self, input_data: Any) -> Any:
        if not self.validate_config():
            raise ValueError("Invalid LLM node configuration")

        llm_call = self.functions["llm_call"]
        if isinstance(input_data, pd.DataFrame):
            texts = input_data[self.config["input_column"]].tolist()
            return [llm_call(self.config["template"], text) for text in texts]
        else:
            return llm_call(self.config["template"], input_data)

    def validate_config(self) -> bool:
        return "template" in self.config


class LLMFilterNode(Node):
    """Node to use LLMs to filter a dataframe."""

    def execute(self, input_data: Any) -> Any:
        llm_filter = self.functions["llm_filter"]
        return llm_filter(input_data, self.config["column"], self.config["prompt"])

    def validate_config(self) -> bool:
        return "column" in self.config and "prompt" in self.config


class FileWriterNode(Node):
    """Node to write data to a file."""

    def execute(self, input_data: Any) -> None:
        with open(self.config["path"], "w") as file:
            file.write(str(input_data))

    def validate_config(self) -> bool:
        return "path" in self.config


class DataFrameOperationNode(Node):
    def execute(self, input_data: Any) -> Any:
        if not isinstance(input_data, pd.DataFrame):
            raise ValueError("Input must be a DataFrame")
        
        operation = self.config['operation']
        args = self.config.get('args', [])
        kwargs = self.config.get('kwargs', {})
        
        if hasattr(input_data, operation):
            method = getattr(input_data, operation)
            if callable(method):
                return method(*args, **kwargs)
            else:
                return method
        else:
            raise ValueError(f"Unknown DataFrame operation: {operation}")

    def validate_config(self) -> bool:
        return 'operation' in self.config
    

"""Helper functions."""

NODE_TYPES: Dict[str, Type[Node]] = {
    "csv": CSVNode,
    "sql": SQLNode,
    "llm": LLMNode,
    "llm_filter": LLMFilterNode,
    "file_writer": FileWriterNode,
    "dataframe_operation": DataFrameOperationNode,
}


def read_sql(query: str, connection_string: str) -> pd.DataFrame:
    """Helper function to execute a read-only SQL query."""
    engine = create_engine(connection_string)
    results = pd.read_sql(query, connection_string)
    engine.dispose()
    return results


def llm_filter(df: pd.DataFrame, column: str, prompt: str) -> pd.DataFrame:
    """Helper function to filter a DataFrame using an LLM yes/no question."""
    results = df[column].apply(
        lambda value: openai_call(prompt + "\n\n----\n\n" + value)
    )
    return df[results.str.lower() == "yes"]


def create_node(
    node_config: Dict[str, Any],
    secrets: Dict[str, str],
    custom_functions: Dict[str, Callable] = None,
) -> Node:
    """Create a node instance based on the configuration. Used in the DAG
    class."""
    node_type = node_config.get("type")
    if node_type not in NODE_TYPES:
        raise ValueError(f"Unknown node type: {node_type}.")

    node_class = NODE_TYPES[node_type]
    node = node_class(node_config, secrets, custom_functions=custom_functions)

    if not node.validate_config():
        raise ValueError(f"Invalid configuration for {node_type} node.")

    return node


"""DAG definition."""


class WordcelDAG:
    """DAG class to define and execute a directed acyclic graph."""

    def __init__(
        self,
        yaml_file: str,
        secrets_file: str = None,
        custom_functions: Dict[str, Callable] = None,
    ):
        """
        Initialize the DAG from a YAML file.
        @param yaml_file: The path to the YAML file containing the DAG configuration.
        @param secrets_file: The path to the YAML file containing the secrets.
        """
        log.warning("This class is still experimental: use at your own risk.")
        self.config = WordcelDAG.load_yaml(yaml_file)
        self.secrets = {}
        if secrets_file is not None:
            self.secrets = WordcelDAG.load_secrets(secrets_file)

        self.graph = self.create_graph()
        self.nodes = self.create_nodes()
        self.functions = self.default_functions
        if custom_functions:
            self.functions.update(custom_functions)

    @property
    def default_functions(self) -> Dict[str, Callable]:
        return {
            "read_sql": read_sql,
            "llm_call": openai_call,
            "llm_filter": llm_filter,
        }

    @staticmethod
    def load_yaml(yaml_file: str) -> Dict[str, Any]:
        """Load a YAML file."""
        with open(yaml_file, "r") as file:
            return yaml.safe_load(file)

    @staticmethod
    def load_secrets(secrets_file: str) -> Dict[str, str]:
        """Load a secrets file."""
        return WordcelDAG.load_yaml(secrets_file)
    
    def save_image(self, path: str) -> None:
        """Save an image of the DAG using graph.draw."""
        nx.draw(self.graph, with_labels=True, font_weight="bold")
        plt.savefig(path)
        plt.close

    def create_graph(self) -> nx.DiGraph:
        """Create a directed graph from the configuration."""
        # Assert that all the `id`s of the nodes are unique first.
        node_ids = [node["id"] for node in self.config["nodes"]]
        assert len(node_ids) == len(set(node_ids)), "Node IDs must be unique."

        # Now create the graph.
        G = nx.DiGraph()
        for node in self.config["nodes"]:
            G.add_node(node["id"], **node)
            if "input" in node:
                G.add_edge(node["input"], node["id"])
        return G

    def create_nodes(self) -> Dict[str, Node]:
        """Create node instances from the graph configuration."""
        nodes = {}
        for node_id, node_config in self.graph.nodes(data=True):
            try:
                nodes[node_id] = create_node(
                    node_config, self.secrets, custom_functions=self.default_functions
                )
            except ValueError as e:
                raise ValueError(f"Error creating node {node_id}: {str(e)}")
        return nodes

    def execute(self) -> Dict[str, Any]:
        """Execute the DAG."""
        results = {}
        for node_id in nx.topological_sort(self.graph):
            log.info(f"Executing node `{node_id}`.")
            node = self.nodes[node_id]
            input_data = results.get(node.config.get("input"))
            results[node_id] = node.execute(input_data)
        return results
