import plotly.express as px
import pandas as pd
pd.set_option('display.max_columns', None)
import numpy as np
# from questionnaire_data_model import Answerset, Answer, Person, Organization, Question, FocusArea, Study, MaturityScore
# import questionnaire_processing_functions as qpf
import rdflib
import compute_maturiy_scores as cms

import generic_radar_plot as grp
import compute_lvl1_maturity_scores as l1cms

import plotly.graph_objects as go

import create_md_report as cmdr
import respondents_tube_in_the_cube as rtc
import organizations_tube_in_the_cube as otc


def generate_report(maturity_model= str,maturity_assessment =str, study= rdflib.URIRef, community= str,
                    responses = str, plot_kind= str, output_directory= str):
    

    # analize respondents
    
    rtc.respondants_tube_in_the_cube(responses= responses,
                                     study= study,
                                     output_dir=output_directory
                                     )
    otc.organizations_tube_in_the_cube(responses=responses,
                                       study=study,
                                       output_dir=output_directory 
                                       )


    # compute overall maturity scores
    overall_maturity_df = cms.compute_maturity_scores(maturity_model=maturity_model, 
                        maturity_assessment=maturity_assessment,
                        responses= responses,
                        study= study,
                        )
    # print(overall_maturity_df.to_markdown)

    # create and save plot

    overall_diagram = grp.generic_radar_plot(overall_maturity_df, plotKind= plotKind)
    filename = output_directory + str(study).split("#",1)[1]+'.svg'
    overall_diagram.savefig(filename, pad_inches= 2)

    community_df, agreements_df, implementation_df =l1cms.compute_lvl1_maturity_scores(maturity_model=maturity_model, 
                                       maturity_assessment=maturity_assessment, 
                                       study=study, 
                                       responses=responses, 
                                       plot_kind= plot_kind,
                                       output_folder=output_directory)
    cmdr.crete_md_report(study=study,
                         output_dir= output_directory,
                         community= community,
                         maturity_df= overall_maturity_df,
                         community_df=community_df,
                         agreements_df= agreements_df,
                         implementation_df= implementation_df
                         )
    
















































