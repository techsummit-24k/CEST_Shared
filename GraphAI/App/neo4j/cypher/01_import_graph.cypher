LOAD CSV WITH HEADERS FROM 'file:///drugs.csv' AS row
MERGE (n:Drug {id: row.drug_id})
SET n.name = row.drug_name,
    n.approval_status = row.approval_status,
    n.drug_class = row.drug_class,
    n.source = row.source;

LOAD CSV WITH HEADERS FROM 'file:///diseases.csv' AS row
MERGE (n:Disease {id: row.disease_id})
SET n.name = row.disease_name,
    n.therapeutic_area = row.therapeutic_area,
    n.source = row.source;

LOAD CSV WITH HEADERS FROM 'file:///genes.csv' AS row
MERGE (n:Gene {id: row.gene_id})
SET n.symbol = row.gene_symbol,
    n.name = row.gene_name,
    n.source = row.source;

LOAD CSV WITH HEADERS FROM 'file:///proteins.csv' AS row
MERGE (n:Protein {id: row.protein_id})
SET n.name = row.protein_name,
    n.uniprot_id = row.uniprot_id,
    n.source = row.source;

LOAD CSV WITH HEADERS FROM 'file:///pathways.csv' AS row
MERGE (n:Pathway {id: row.pathway_id})
SET n.name = row.pathway_name,
    n.source = row.source;

LOAD CSV WITH HEADERS FROM 'file:///evidence.csv' AS row
MERGE (n:Publication {id: row.publication_id})
SET n.title = row.title,
    n.year = toInteger(row.year),
    n.pmid = row.pmid,
    n.source = row.source;

LOAD CSV WITH HEADERS FROM 'file:///drug_targets_protein.csv' AS row
MATCH (drug:Drug {id: row.drug_id})
MATCH (protein:Protein {id: row.protein_id})
MERGE (drug)-[r:TARGETS]->(protein)
SET r.action = row.action,
    r.evidence_score = toFloat(row.evidence_score),
    r.evidence_type = row.evidence_type,
    r.source = row.source;

LOAD CSV WITH HEADERS FROM 'file:///protein_encoded_by_gene.csv' AS row
MATCH (protein:Protein {id: row.protein_id})
MATCH (gene:Gene {id: row.gene_id})
MERGE (protein)-[r:ENCODED_BY]->(gene)
SET r.source = row.source;

LOAD CSV WITH HEADERS FROM 'file:///gene_associated_with_disease.csv' AS row
MATCH (gene:Gene {id: row.gene_id})
MATCH (disease:Disease {id: row.disease_id})
MERGE (gene)-[r:ASSOCIATED_WITH]->(disease)
SET r.evidence_score = toFloat(row.evidence_score),
    r.evidence_type = row.evidence_type,
    r.source = row.source;

LOAD CSV WITH HEADERS FROM 'file:///drug_treats_disease.csv' AS row
MATCH (drug:Drug {id: row.drug_id})
MATCH (disease:Disease {id: row.disease_id})
MERGE (drug)-[r:TREATS]->(disease)
SET r.approval_status = row.approval_status,
    r.evidence_score = toFloat(row.evidence_score),
    r.evidence_type = row.evidence_type,
    r.source = row.source;

LOAD CSV WITH HEADERS FROM 'file:///gene_participates_pathway.csv' AS row
MATCH (gene:Gene {id: row.gene_id})
MATCH (pathway:Pathway {id: row.pathway_id})
MERGE (gene)-[r:PARTICIPATES_IN]->(pathway)
SET r.source = row.source;