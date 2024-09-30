from generate_report import generate_report
from responses_to_ld import answerset_to_rdf

# this function performs the whole process from importing the xml response
# to adding the results to the responses rdf graph and generating the report

def import_write_results_generate_reports(input_xml = str, 
                                          input_rdf=str,
                                          output_rdf = str,
                                          serialization='ttl',
                                          maturity_model= str,
                                          maturity_assessment =str, 
                                          study= rdflib.URIRef, 
                                          community= str,
                                          responses = str, 
                                          plot_kind= str, 
                                          output_directory= str) :
    
    answerset_to_rdf(input_xml= input_xml, 
                     input_rdf= input_rdf,
                     output_rdf= output_rdf,
                     serialization = serialization)
    
    generate_report(maturity_model= maturity_model ,
                    maturity_assessment =maturity_assessment, 
                    study= study, 
                    community= community,
                    responses = responses, 
                    plot_kind= plot_kind, 
                    output_directory= output_directory)
    
