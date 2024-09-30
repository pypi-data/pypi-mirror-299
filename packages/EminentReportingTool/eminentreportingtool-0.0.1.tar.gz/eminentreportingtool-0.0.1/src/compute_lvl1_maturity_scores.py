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

from subcapability_radar_plot import subcapability_radar_plot
from raw_data_to_maturityscore import raw_data_to_MaturityScore


def compute_lvl1_maturity_scores(maturity_model= str, maturity_assessment = str, responses= str, study= URIRef, plot_kind = str, output_folder= str):
    g= Graph()
    g.parse(maturity_model)
    g.parse(maturity_assessment)
    g.parse(responses)
    
    emar_ns= Namespace("http://eminent.intnet.eu/maturity_assessment_results#")
    ema_ns = Namespace("http://eminent.intnet.eu/maturity_assessment#")
    emm_ns = Namespace("http://eminent.intnet.eu/maturity_model#")
    sgam_ns = Namespace("http://eminent.intnet.eu/sgam#")
    g.bind("emar", emar_ns)
    g.bind("ema", ema_ns)
    g.bind("emm", emm_ns)
    g.bind("sgam", sgam_ns)

    # query to find all level 1 capabilities
    lvl1_capability_query  = """
    SELECT DISTINCT ?capability ?prefLabel
    WHERE {
        ?capability rdf:type emm:Capability .
        ?capability skos:prefLabel ?prefLabel .
        FILTER NOT EXISTS {
            ?capability dcterms:isPartOf ?otherCapability .
        }
    }"""

    dimension_per_lvl1_capability_query  = """
    SELECT DISTINCT ?dimension ?prefLabel
    WHERE {
        ?dimension rdf:type emm:Dimension .
        ?dimension skos:prefLabel ?prefLabel .
        ?dimension dcterms:isPartOf* ?capability .

    }"""

    desired_order_community = [
        "Community Growth process",
        "Community Growth people and organization",
        "Community Growth Information",
        "Community Growth resources",
        "Knowledge Retention process",
        "Knowledge Retention people and organization",
        "Knowledge Retention Information",
        "Knowledge Retention resources",
        "Diversity of Perspectives process",
        "Diversity of Perspectives people and organization",
        "Diversity of Perspectives Information",
        "Diversity of Perspectives resources",
        
        ]

    desired_order_agreements = [
        "Integration Profile Establishment process",
        "Integration Profile Establishment people and organization",
        "Integration Profile Establishment Information",
        "Integration Profile Establishment resources",
        "Standardization process",
        "Standardization people and organization",
        "Standardization Information",
        "Standardization resources",
        "Compliance Testing process",
        "Compliance Testing people and organization",
        "Compliance Testing Information",
        "Compliance Testing resources",        
    ]

    desired_order_implementation = [
        "User Base Growth process",
        "User Base Growth people and organization",
        "User Base Growth Information",
        "User Base Growth resources",        
        "Operational Alignment process",
        "Operational Alignment people and organization",
        "Operational Alignment Information",
        "Operational Alignment resources",
        "Tool, Product and Reference Implementation Development process",
        "Tool, Product and Reference Implementation Development people and organization",
        "Tool, Product and Reference Implementation Development Information",
        "Tool, Product and Reference Implementation Development resources",
        "Market Creation process",
        "Market Creation people and organization",
        "Market Creation Information",
        "Market Creation resources",        
    ]

    # query to find all scores associated with a specific study and a specific capability and/ordimension
    collect_scores_query = """select ?capabilityOrDimension ?result where {{ 
        ?answer sosa:hasResult/emm:maturityScore ?result .
        ?answer dcterms:isPartOf* ?study .
        ?answer sosa:usedProcedure/ema:measures/dcterms:isPartOf* ?capabilityOrDimension .
    }}"""


    #innittiate maturity data frame
    

    # lvl1_capabilities = g.query(lvl1_capability_query)
    lvl1cap= g.query(lvl1_capability_query)
    for row in lvl1cap:
        # print(f"{row.capability} : {row.prefLabel}")

        maturity_df = pd.DataFrame(dict(
        dimension =[],
        maturity_avg=[],
        maturity_median= [],
        maturity_mode=[],
        number_of_answers=[],
        stddev = [],
        number_of_unsure= [])
        )

        dim = g.query(dimension_per_lvl1_capability_query, initBindings={'study': URIRef(study), 'capability' : URIRef(row.capability)} )
        
        for d in dim:
            scores= g.query(collect_scores_query, initBindings={'study': URIRef(study), 'capabilityOrDimension' : URIRef(d.dimension)} )
            raw_data =[]
            for s in scores:

                raw_data.append(s.result.toPython())
            
            print(raw_data)

            maturity_score= raw_data_to_MaturityScore(raw_data=raw_data)
            maturity_df.loc[len(maturity_df.index)] = [str(d.prefLabel), 
                                                        maturity_score.averageScore, 
                                                        maturity_score.medianScore,
                                                        maturity_score.modeScore,
                                                        maturity_score.totalAnswers,
                                                        maturity_score.standardDeviation,
                                                        maturity_score.numberOfUnsure
                                                        ]
            
        if str(row.capability) == 'http://eminent.intnet.eu/maturity_model#CommunityFacilitation':
            maturity_df['dimension']=pd.Categorical(maturity_df['dimension'], categories=desired_order_community, ordered=True)
            maturity_df= maturity_df.sort_values(by='dimension')
            community_facilitation_df= maturity_df
            
        elif str(row.capability) == 'http://eminent.intnet.eu/maturity_model#TechnicalAgreements':
            maturity_df['dimension']=pd.Categorical(maturity_df['dimension'], categories=desired_order_agreements, ordered=True)
            maturity_df= maturity_df.sort_values(by='dimension')
            technical_agreements_df = maturity_df
            
        elif str(row.capability) == 'http://eminent.intnet.eu/maturity_model#Implementation':
            maturity_df['dimension']=pd.Categorical(maturity_df['dimension'], categories=desired_order_implementation, ordered=True)
            maturity_df= maturity_df.sort_values(by='dimension')
            implementation_df = maturity_df
        
        

        plot = subcapability_radar_plot(maturitydf=maturity_df, plotKind=plot_kind, capability= row.capability) 
        filename = output_folder + str(study).split("#",1)[1]+'_' +str(row.capability).split("#",1)[1] + '.svg'
        plot.savefig(filename, pad_inches= 2)
        plot.show()
    print(community_facilitation_df)
    print(technical_agreements_df)
    print(implementation_df)    
    return community_facilitation_df , technical_agreements_df, implementation_df





