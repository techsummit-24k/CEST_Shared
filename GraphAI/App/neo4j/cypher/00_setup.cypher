CREATE CONSTRAINT drug_id_unique IF NOT EXISTS
FOR (n:Drug) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT disease_id_unique IF NOT EXISTS
FOR (n:Disease) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT gene_id_unique IF NOT EXISTS
FOR (n:Gene) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT protein_id_unique IF NOT EXISTS
FOR (n:Protein) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT pathway_id_unique IF NOT EXISTS
FOR (n:Pathway) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT publication_id_unique IF NOT EXISTS
FOR (n:Publication) REQUIRE n.id IS UNIQUE;

CREATE INDEX drug_name_index IF NOT EXISTS
FOR (n:Drug) ON (n.name);

CREATE INDEX disease_name_index IF NOT EXISTS
FOR (n:Disease) ON (n.name);

CREATE INDEX gene_symbol_index IF NOT EXISTS
FOR (n:Gene) ON (n.symbol);

SHOW CONSTRAINTS;

SHOW INDEXES;