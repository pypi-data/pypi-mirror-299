from rdflib import Graph, Namespace, URIRef, Literal, BNode
from rdflib.namespace import FOAF, DCTERMS, DCAT, PROV, OWL, RDFS, RDF, XMLNS, SKOS, SOSA, ORG, SSN
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from mpl_toolkits.mplot3d import Axes3D 
import matplotlib.pyplot as plt 
import numpy as np 
from pylab import *

import pickle


def respondants_tube_in_the_cube (responses: text, study: str, output_dir : str):
    ################################
    ##### setting up the graph #####
    ################################
    study_name =str(study).split("#",1)[1]
    g= Graph()
    g.parse(responses)

    emar_ns= Namespace("http://eminent.intnet.eu/maturity_assessment_results#")
    ema_ns = Namespace("http://eminent.intnet.eu/maturity_assessment#")
    emm_ns = Namespace("http://eminent.intnet.eu/maturity_model#")
    sgam_ns = Namespace("http://eminent.intnet.eu/sgam#")
    
    g.bind("emar", emar_ns)
    g.bind("ema", ema_ns)
    g.bind("emm", emm_ns)
    g.bind("sgam", sgam_ns)

    ##########################
    ##### gathering data #####
    ##########################

    # query to find all scores associated with a specific study and a specific capability and/ordimension
    tube_in_the_tube_query = """select distinct ?answerset ?person ?domain ?zone ?layer where {{
        ?answerset dcterms:isPartOf ?study . 
        ?answerset prov:wasQuotedFrom ?person .
        ?answerset prov:wasQuotedFrom/ema:areaOfExpertise/ema:inDomain ?domain .
        ?answerset prov:wasQuotedFrom/ema:areaOfExpertise/ema:inZone ?zone .
        ?answerset prov:wasQuotedFrom/ema:areaOfExpertise/ema:onLayer ?layer .
        
    }}"""

    tube= g.query(tube_in_the_tube_query, initBindings={'study': URIRef(study)})
    tube_df = pd.DataFrame(dict(
        person=[],
        domain=[],
        zone= [],
        layer=[])
        )

    for t in tube :
        # print(print(f" {t.person} : {t.domain} : {t.zone} : {t.layer}"))
        tube_df.loc[len(tube_df.index)] = [t.person, 
                                                t.domain.split("#", 1)[1], 
                                                t.zone.split("#", 1)[1],
                                                t.layer.split("#", 1)[1]
                                                ] 

    df = pd.DataFrame(tube_df)
    # Count occurrences of each combination of keywords
    keyword_counts = df.groupby(['domain', 'zone', 'layer']).size().reset_index(name='Count')
    # print(keyword_counts)

    ####################################################
    ##### preprocessing for graphic representation #####
    ####################################################

    zone_map = {
        'Process': 1,
        'Field' : 2,
        'Operation' : 3,
        'Enterprise' : 4,
        'Market' : 5
    }

    domain_map = {
        'CustomerPremises' : 1,
        'DER' : 2,
        'Distribution' : 3,
        'Transmission' : 4,
        'Generation' : 5
    }

    layer_map = {
        'ComponentLayer' : 1,
        'CommunicationLayer' : 2,
        'InformationLayer' : 3,
        'FunctionLayer' : 4,
        'BusinessLayer' : 5,
        'RegulatoryLayer' : 6, 
    }



    keyword_counts['zone']= keyword_counts['zone'].map(zone_map)
    keyword_counts['domain']= keyword_counts['domain'].map(domain_map)
    keyword_counts['layer']= keyword_counts['layer'].map(layer_map)


    # assigning the data the right axes 
    y = keyword_counts['zone']
    x = keyword_counts['domain']
    z = keyword_counts['layer']
    colo = keyword_counts['Count']
    

    ################################
    ##### creating the diagram #####
    ################################
    # creating figures 
    fig = plt.figure(figsize=(10, 10)) 
    ax = fig.add_subplot(111, projection='3d') 
    
    # setting color bar 
    color_map = cm.ScalarMappable(cmap=cm.Greens) 
    color_map.set_array(colo) 
    
    # creating the heatmap 
    img = ax.scatter(x, y, z, marker='o', c = colo,
                    s=400,depthshade=False ) 
    plt.colorbar(img, ax= ax, pad =0.1) 

    # adding title and labels 
    ax.set_title("respondents distribution") 
    ax.set_ylabel('zone') 
    ax.yaxis.set_major_locator(matplotlib.ticker.FixedLocator([1,2,3,4,5]))
    ax.yaxis.set_major_formatter(matplotlib.ticker.FixedFormatter(
        ['Process', 'Field', 'Operation', 'Enterprise', 'Market']
        ))

    ax.set_xlabel('domain') 
    ax.xaxis.set_major_locator(matplotlib.ticker.FixedLocator([1,2,3,4,5]))
    ax.xaxis.set_major_formatter(matplotlib.ticker.FixedFormatter(
        ['Customer', 'DER', 'Distribution', 'Transmission', 'Generation']
        ))

    ax.set_zlabel('layer')
    ax.zaxis.set_major_locator(matplotlib.ticker.FixedLocator([1,2,3,4,5,6]))
    ax.zaxis.set_major_formatter(matplotlib.ticker.FixedFormatter(
        ['Component', 'Communication', 'Information', 'Function', 'Business', 'Framework']
        ))

    # ax.xticks(np.arange(5), ['Process', 'Field', 'Operation', 'Enterprise', 'Market'])

    ax.set_xlim([1, 5])
    ax.tick_params(axis='x', pad=3)
    ax.set_ylim([1, 5])
    ax.tick_params(axis='y', pad=3)
    ax.set_zlim([1, 6])
    ax.tick_params(axis='z', pad=3)

    # displaying plot 
    ax.view_init(elev=70, azim=45)
    # plt.show()
    figname= output_dir+ study_name+'_respondents_tube_in_the_cube.png' 
    plt.savefig(figname)



