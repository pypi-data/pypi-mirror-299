import xml.etree.ElementTree as ET
import xml.etree.ElementTree as ET
from rdflib import Graph, Namespace, URIRef, Literal, BNode
from rdflib.namespace import FOAF, DCTERMS, DCAT, PROV, OWL, RDFS, RDF, XMLNS, SKOS, SOSA, ORG, SSN
import pandas as pd
pd.set_option('display.max_columns', None)


from datetime import date, datetime, time, timedelta
from typing import List, Optional
from pydantic import BaseModel
from typing import Union
import numpy as np

import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib

# from generic_radar_plot import generic_radar_plot
from raw_data_to_maturityscore import raw_data_to_MaturityScore



def compute_maturity_scores(maturity_model= str, maturity_assessment = str, responses= str, study= URIRef):
    g= Graph()
    g.parse(maturity_model)
    g.parse(maturity_assessment)
    g.parse(responses)

    # print(study)
    
    emar_ns= Namespace("http://eminent.intnet.eu/maturity_assessment_results#")
    ema_ns = Namespace("http://eminent.intnet.eu/maturity_assessment#")
    emm_ns = Namespace("http://eminent.intnet.eu/maturity_model#")
    sgam_ns = Namespace("http://eminent.intnet.eu/sgam#")
    g.bind("emar", emar_ns)
    g.bind("ema", ema_ns)
    g.bind("emm", emm_ns)
    g.bind("sgam", sgam_ns)



    #query to find all level 2 capabilities
    lvl2_capability_query  = """
    SELECT DISTINCT ?capability ?prefLabel
    WHERE {
        ?capability rdf:type emm:Capability .
        ?capability skos:prefLabel ?prefLabel .
        ?capability dcterms:isPartOf ?b .
    }"""



    desired_order_lvl1 = [
           'Community Growth',
           'Knowledge Retention',
           'Diversity of Perspectives',
           'Integration Profile Establishment',
           'Standardization',
           'Compliance Testing',
           'User Base Growth',
           'Operational Alignment',
           'Tool, Product and Reference Implementation Development',
           'Market Creation'
    ]

 
    # query to find all scores associated with a specific study and a specific capability and/ordimension
    collect_scores_query = """select ?result where {{ 
        ?answer sosa:hasResult/emm:maturityScore ?result .
        ?answer dcterms:isPartOf* ?study .
        ?answer sosa:usedProcedure/ema:measures/dcterms:isPartOf* ?capabilityOrDimension .
    }}"""


    #innittiate maturity data frame
    maturity_df = pd.DataFrame(dict(
        capability=[],
        maturity_avg=[],
        maturity_median= [],
        maturity_mode=[],
        number_of_answers=[],
        stddev = [],
        number_of_unsure= [])
        )

    lvl2_capabilities = g.query(lvl2_capability_query)


    for row in lvl2_capabilities:

        scores= g.query(collect_scores_query, 
                        initBindings={'study': URIRef(study), 
                                      'capabilityOrDimension' : URIRef(row.capability)
                                      } )

        raw_data= []
        for r in scores:

            raw_data.append(r.result.toPython())

        
        maturity_score= raw_data_to_MaturityScore(raw_data=raw_data)

        maturity_df.loc[len(maturity_df.index)] = [str(row.prefLabel), 
                                                        maturity_score.averageScore, 
                                                        maturity_score.medianScore,
                                                        maturity_score.modeScore,
                                                        maturity_score.totalAnswers,
                                                        maturity_score.standardDeviation,
                                                        maturity_score.numberOfUnsure
                                                        ] 

    # print(maturity_df)
    
    maturity_df['capability']=pd.Categorical(maturity_df['capability'], 
                                             categories=desired_order_lvl1, 
                                             ordered=True)
    maturity_df= maturity_df.sort_values(by='capability')


    return maturity_df
        



