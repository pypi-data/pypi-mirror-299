import luigi
from neo4j import GraphDatabase
from typing import Callable, Any, Optional
from .graph import Graph, Node, Relationship

class Neo4jTarget(luigi.Target):
    def __init__(self, database: GraphDatabase.driver, graph_id: str, 
                 marshaler: Optional[Callable[[Any], Graph]] = None,
                 unmarshaler: Optional[Callable[[Graph], Any]] = None):
        """
        :param database: Neo4j driver instance to connect to the database.
        :param graph_id: Unique identifier for the graph or subgraph.
        :param marshaler: Callable to transform any object into a Graph object.
        :param unmarshaler: Callable to transform a Graph object back into any object.
        """
        self.database = database
        self.graph_id = graph_id
        self.marshaler = marshaler or self.default_marshaler
        self.unmarshaler = unmarshaler or self.default_unmarshaler
        
        # Ensure the database is accessible
        with self.database.session() as session:
            session.run("RETURN 1")

    def default_marshaler(self, data: Any) -> Graph:
        """
        Default method to convert any input data to a Graph object if no custom marshaller is provided.
        Expects data to be in Graph format.
        """
        if isinstance(data, Graph):
            return data
        raise TypeError(f"Cannot marshal {type(data)} into a Graph")

    def default_unmarshaler(self, graph: Graph) -> Any:
        """
        Default method to convert a Graph object into any output format if no custom unmarshaller is provided.
        """
        return graph  # No transformation by default

    def exists(self):
        """
        Check if the graph with the given graph_id exists in the database.
        """
        query = """
        MATCH (n) 
        WHERE n.graph_id = $graph_id 
        RETURN n LIMIT 1
        """
        with self.database.session() as session:
            result = session.run(query, graph_id=self.graph_id)
            return result.single() is not None

    def put(self, graph_data: Any):
        """
        Store the graph (transformed from any data using marshaler) into the database.

        :param graph_data: Input data to be transformed into a Graph using marshaler.
        """
        graph = self.marshaler(graph_data)  # Transform the input into a Graph
        with self.database.session() as session:
            query = """
            MATCH (n {graph_id: $graph_id})
            DETACH DELETE n
            """
            session.run(query, graph_id=self.graph_id)
            for node in graph.nodes:
                label = ":".join(node.labels)
                properties = node.properties
                properties["graph_id"] = self.graph_id  # Tag nodes with graph_id
                query = f"CREATE (n:{label} $properties)"
                session.run(query, properties=properties)

            for relationship in graph.relationships:
                source_uuid = str(relationship.source.uuid)
                target_uuid = str(relationship.target.uuid)
                type = relationship.type
                query = f"""
                MATCH (a {{uuid: $source_uuid, graph_id: $graph_id}}), 
                      (b {{uuid: $target_uuid, graph_id: $graph_id}})
                CREATE (a)-[r:{type} $properties]->(b)
                """
                session.run(query, source_uuid=source_uuid, target_uuid=target_uuid, graph_id=self.graph_id, properties=relationship.properties)

    def get(self) -> Any:
        """
        Retrieve the graph from the database, and transform it into the desired output format using unmarshaler.

        :return: Any object obtained by transforming the retrieved Graph object using unmarshaler.
        """
        with self.database.session() as session:
            # Retrieve nodes
            nodes_query = "MATCH (n) WHERE n.graph_id = $graph_id RETURN n"
            nodes_result = session.run(nodes_query, graph_id=self.graph_id)
            nodes = {}
            for record in nodes_result:
                node_labels = list(record["n"].labels)
                node_properties = { k:v for k,v in dict(record["n"]).items() if k not in ['uuid','name'] }
                node_uuid = dict(record["n"]).get('uuid')
                node_name = dict(record["n"]).get('name')
                nodes[node_uuid] = Node(labels=node_labels, name=node_name, uuid=node_uuid, properties=node_properties)

            # Retrieve relationships
            relationships = []
            relationships_query = """
            MATCH (s)-[r]->(t)
            WHERE s.graph_id = $graph_id AND t.graph_id = $graph_id
            RETURN s.uuid AS source_uuid, t.uuid AS target_uuid, r AS r
            """
            relationships_result = session.run(relationships_query, graph_id=self.graph_id)
            for record in relationships_result:
                rel_source = nodes[record["source_uuid"]]
                rel_target = nodes[record["target_uuid"]]
                rel_type = record["r"].type
                rel_properties = { k:v for k,v in dict(record["r"].items()).items() }
                relationships.append(Relationship(source=rel_source, type=rel_type, target=rel_target, properties=rel_properties))

            graph = Graph(nodes=nodes.values(), relationships=relationships)
            return self.unmarshaler(graph)  # Transform the Graph into the desired output format