import biocypher
import neo4j_utils as nu


class BioCypherAdapter:
    def __init__(
        self,
        dirname=None,
        db_name="neo4j",
        id_batch_size: int = int(1e6),
        user_schema_config_path="config/schema_config.yaml",
    ):

        self.db_name = db_name
        self.id_batch_size = id_batch_size

        # write driver
        self.bcy = biocypher.Driver(
            offline=True,  # set offline to true,
            # connect to running DB for input data via the neo4j driver
            user_schema_config_path=user_schema_config_path,
            delimiter=",",
        )
        # start writer
        self.bcy.start_bl_adapter()
        self.bcy.start_batch_writer(dirname=dirname, db_name=self.db_name)

        # read driver
        self.driver = nu.Driver(
            db_name="neo4j",
            config="config/neo4j_config.yaml",
            multi_db=False,  # set to True if on Neo4j>4.0
            max_connection_lifetime=7200,
        )

    def write_to_csv_for_admin_import(self):
        """
        Write nodes and edges to admin import csv files.
        """

        self.write_nodes()
        self.write_edges()

    def write_nodes(self):
        """
        Write nodes to csv files.
        """

        # get node labels
        node_labels = ["Subject", "Phenotype"]

        # write nodes
        for node_label in node_labels:
            # generator
            def node_generator():
                with self.driver.session() as session:
                    query = f"MATCH (n:{node_label}) RETURN n.id as id"
                    result = session.run(query)
                    for row in result:
                        _id = row["id"]
                        _label = node_label
                        _properties = {}
                        yield (_id, _label, _properties)

            self.bcy.write_nodes(node_generator(), db_name=self.db_name)

    def write_edges(self):
        """
        Write edges to csv files.
        """

        # generator
        def edge_generator():
            with self.driver.session() as session:
                query = (
                    "MATCH (s:Subject)<-[:HAS_ENROLLED]-(:Project {acronym: 'MIMIC'}) "
                    "WITH s "
                    "MATCH (s:Subject)<-[:BELONGS_TO_SUBJECT]-"
                    "(:Biological_sample)-[:SPLITTED_INTO]->(:Analytical_sample)-"
                    "[:HAS_PHENOTYPE]->(p:Phenotype) "
                    "RETURN s, p"
                )
                result = session.run(query)
                for row in result:
                    _src_id = row["s"]["id"]
                    _tar_id = row["p"]["id"]
                    _label = "HAS_PHENOTYPE"
                    yield (None, _src_id, _tar_id, _label, {})

        # write edges
        self.bcy.write_edges(edge_generator(), db_name=self.db_name)
