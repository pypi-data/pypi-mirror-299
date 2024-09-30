# EminentReportingTool
tool for generating reports out of eminent questionnaire data

## Functions

This package contains several functions that each perform different functions in managing eminent data. 

There are two important input artifacts that these functions use:
- export of the EUSurvey responses in XML
- a spreadsheet with the capability and maturity model.

### import_write_results_generate_reports()

This function performs all the actions supported by this package.

It takes as inputs:

- input_xml =str,  path to input xml 
- input_rdf= str, path to rdf file to which the results need to be added
- output_rdf = str, path to the output rdf
- serialization= str, syntax to which output rdf needs to be serialized,  default 'ttl',
- maturity_model= str, path to maturity model to be used,
- maturity_assessment =str, path to maturity assessment to be used, 
- study= rdflib.URIRef, uri of the study
- community= str, name of the community
- responses = str, path to the responses to be used for generating the report, 
- plot_kind= str, which statistical method should be used for the plots, default 'maturity_avg'
- output_directory= str, directory to which the files need to be written

### IMM_to_ld()

The function assumes the spreadsheet has a format similar to that found in ```./tests/EminentV2.1.xlsx```. It contains a list of characteristics, that are associated with their maturity level, the dimension they describe, the leevel 2 capability they belong to and the level 1 capability they belong to and then generates the tripples for each of those resources

the IMM_to_ld function takes as input:
- input_spreadsheet : string, the path to the spreadsheet containing the capability model and the maturity model
- namespace : string, the namespace within which the maturity model will need to be defined
- output_rdf : string, the path to which the rdf representation needs to be written

output:
- rdf graph object containing the tripples describing the maturity model

### survey_to_ld()

This function takes the survey as input and generates an rdf graph that contains the questions and their relationships to the maturity model. Only use this function when a change has been made to the survey and a new version needs to be generated

This function takes as input:
- input_xml = str,  path to the survey export of the EUSurvey responses in XML
- version_number= str,  the new version number of the survey
- output_rdf= str, the path to which the rdf representation needs to be written
- serialization = 'ttl', the way the graph should be serialized, default is 'ttl' (see rdflib documentation for other options)\

output:
- rdf graph object containing the tripples describing the questionnaire and which question measures which dimension in the IMM

### responses_to_ld()

This function takes an EMINENT result export from EUSurvey and generates an rdf graph, and if desired adds that to an existing rdf graph of results.

- input_xml = str, file path to the xml export of EU Survey
- input_rdf=None , file path to existing rdf data to which the results should be added
- output_rdf= str, file path to which the resulting rdf graph should be written
- serialization= 'ttl' , format in which the rdf graph should be serialized, default is ttl

output:
- none

### classify_characteristic()

This function takes a description of a characteristic and returns the uri of the characterisitic to which it belongs. This function is to compensate for the fact that the maturity model (including characteristic descriptions) is developed outside of EUSurvey, but EUSurvey gives these a separate, new ID as a choice answer, that needs to be matched to the characteristic in the maturity model ontology/knowledgegrapgh. Unfortunately this function requires a lot of business logic to make this work (see notes in the source code, including a suggestion for quicker, more elegant code if you can assume the descriptions are an exact match)

input: 
- desctiption: str, the textual description of a characteristic

output:
- characteristic_uri : rdfLib.URIRef, the URI to which that identifies the characteristic described by the input

### compute_lvl1_maturity_scores()

This function will, for a given capability and a study, compute the maturity score per subcapability+dimension based on the responses given for that study.

input:
- maturity_model= str, file path pointing to the maturity model (represented as rdf) to be used 
- maturity_assessment = str, file path pointing to the maturity assessment (represented as rdf) to be used 
- responses= str, file path pointing to the responses (represented as rdf) to be used 
- study= URIRef, uri of the study for which the score is to be computed
- plot_kind = str, type of plot that needs to be produced. Based on method for calculating maturity score
    - valid values are : 'maturity_median','maturity_mode' and 'maturity_avg'
- output_folder = None, folder to which the resulting diagrams need to be saved


output:
- plot, the diagram object produced 


### compute_maturity_scores()

This function will, for a given study, compute the maturity score per subcapability based on the responses given for that study.

input:
- maturity_model= str, file path pointing to the maturity model (represented as rdf) to be used 
- maturity_assessment = str, file path pointing to the maturity assessment (represented as rdf) to be used 
- responses= str, file path pointing to the responses (represented as rdf) to be used 
- study= URIRef, uri of the study for which the score is to be computed
- plot_kind = str, type of plot that needs to be produced. Based on method for calculating maturity score
    - valid values are : 'maturity_median','maturity_mode' and 'maturity_avg'
- output_folder = None, folder to which the resulting diagrams need to be saved


output:
- plot, the diagram object produced 

### qid_to_answerValue()

This function is used by responses_to_ld() to retrieve the string value of an answer based on the aid value (the id of the multiple choice option) of a response. In this format a response is nothing more than a combination of a qid and an aid. 

input:
- AS: an answerSet subtree of the raw EUSurvey export xml format
- root: the root element of the tree of the raw EUSurvey export xml format
- target_qid: the qid of the resonse for which we'd like to receive the anser value. within an answerset this value is unique

### raw_data_to_maturityscore()

This function takes the a list of the responses (either an integer or 'unsure' ) and computes the average, median, mode, standard deviation,  and the number of times a respondant answered 'unsure'.

input:
- raw_data : list, a list of integer- and 'unsure' responses given to a specific question

output:
- MaturityScore object with the computed values


### subcapability_radar_plot()


input:
- maturitydf: DataFrame, a dataframe containing the maturity scores per dimension
- plotKind: str, the kind of plot desired
- capability, rdfLib.URIref, the uri of the capability 


output:
- fig, the diagram object containing the radarplot of maturity scores