from rdflib import Graph, Namespace, URIRef, Literal, BNode
from rdflib.namespace import FOAF, DCTERMS, DCAT, PROV, OWL, RDFS, RDF, XMLNS, SKOS, SOSA, ORG, SSN

def classify_characteristic(description = str):
    # this function takes a description of a characteristic and returns the related characteristic
    # uri.
    # it is increadibly ugly and slow because there are mismaches between the characteristic descriptions
    # in the ontology and those in the questionnaire, That is why we have to loop through all tripples
    # manipulate the strings (remove spaceS and special characters, all lowe case etc) and then make
    # comparison

    # if you can assume the descriptions match, the following code would do the same trick and be much faster:

    # for s, p, o in imm_g.triples((None,  SKOS.definition, Literal(description))):
    #     characteristic_uri = s
    #
    # return s    
    emm_ns = Namespace("http://eminent.intnet.eu/maturity_model#")

    imm_g = Graph()
    imm_g.parse('./tests/imm.ttl')

    bad_characters= ['.',',', ' ', '\n',"'","’", 'â€™']

    characteristic_uri = None

    bad_resources_0 = {
        "There are no resources available for Community Growth . Individuals who do participate in Community Growth do so voluntarily in their own time." : "CommunityGrowth_resources_0",
        "There are no resources available for Compliance Testing . Individuals who do participate in Compliance Testing do so voluntarily in their own time.": "ComplianceTesting_resources_0",
        "There are no resources available for Diversity of Perspectives . Individuals who do participate in Diversity of Perspectives do so voluntarily in their own time.": "DiversityofPerspectives_resources_0",
        "There are no resources available for Integration Profile Establishment . Individuals who do participate in Integration Profile Establishment do so voluntarily in their own time." : "ProfileEstablishment_resources_0",
        "There are no resources available for Knowledge Retention . Individuals who do participate in Knowledge Retention do so voluntarily in their own time.": "KnowledgeRetention_resources_0",
        "There are no resources available for Market Creation . Individuals who do participate in Market Creation do so voluntarily in their own time.": "MarketCreation_resources_0",
        "There are no resources available for Operational Alignment . Individuals who do participate in Operational Alignment do so voluntarily in their own time.": "OperationalAlignment_resources_0",
        "There are no resources available for Standardization . Individuals who do participate in Standardization do so voluntarily in their own time.": "Standardization_resources_0",
        "There are no resources available for Tool, Product and Reference Implementation Development . Individuals who do participate in Tool, Product and Reference Implementation Development do so voluntarily in their own time." : "Tool,ProductandReferenceImplementationDevelopment_resources_0",
        "There are no resources available for User Base Growth . Individuals who do participate in User Base Growth do so voluntarily in their own time.": "UserBaseGrowth_Information_0",
        "There is little to no process documentation, -governance, or -ownership for Community Growth. Progress on Community Growth is based on individualâ€™s knowledge, manual interventions and with unpredictable results": "CommunityGrowth_process_1",
        "Diversity of Perspectives' relationship to resources is defined and requirements are part of the investment planning process. Most individuals performing work for Diversity of Perspectives are compensated for their effort by the organization they represent.": "DiversityofPerspectives_resources_3"
    }

    if description in bad_resources_0 :
        characteristic_uri = emm_ns[str(bad_resources_0[description])]
        # print(type(characteristic_uri))

    else:
        description=description.lower()
        for i in bad_characters:
            description= description.replace(i, '')

        for s, p, o in imm_g.triples((None,  SKOS.definition, None)):
            o = o.lower()
            for i in bad_characters:
                o=o.replace(i, '')

                if o==description:
                    characteristic_uri= s
    if characteristic_uri == None:
        characteristic_uri=emm_ns.nonsense  # this should never happen         
    return characteristic_uri

