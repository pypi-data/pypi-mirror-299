import xml.etree.ElementTree as ET
import pandas as pd
from rdflib import Graph, Namespace, URIRef, Literal, BNode
from rdflib.namespace import FOAF, DCTERMS, DCAT, PROV, OWL, RDFS, RDF, XMLNS, SKOS, SOSA, ORG, SSN

from pydantic import BaseModel


def imm_to_ld ( input_spreadsheet = str, namespace=str , output_rdf = str):

    # parse excel file and create data frame
    maturity_model = pd.read_excel(input_spreadsheet, 'eminent v3 generated') 
    # make sure indexes pair with number of rows
    maturity_model= maturity_model.reset_index()

    # innitiate graph
    graph = Graph()

    emm_ns = Namespace(namespace)
    graph.bind("emm", emm_ns)

    # loop over all rows and add tripplea for each row
    # can probably be optimized
    for index, characteristic in maturity_model.iterrows() :

        lvl1_name = str(characteristic['lvl 1 capability'])
        lvl1_uri = emm_ns[str(characteristic['lvl 1 capability']).replace(" ", "").replace(",", "")]

        lvl2_name = str(characteristic['lvl 2 capability'])
        lvl2_uri = emm_ns[str(characteristic['lvl 2 capability']).replace(" ", "").replace(",", "")]

        dimension_name = (str(characteristic['lvl 2 capability']) + ' ' +
                               str(characteristic['Dimension']))
        dimension_uri = emm_ns[str(characteristic['lvl 2 capability']).replace(" ", "").replace(",", "") + '_' +
                               str(characteristic['Dimension']).replace(" ", "").replace(",", "")]
        
        characteristic_name = (str(characteristic['lvl 2 capability']) + ' ' +
                               str(characteristic['Dimension'])+ ' ' +
                               str(characteristic['Level']))
        characteristic_uri = emm_ns[str(characteristic['lvl 2 capability']).replace(" ", "").replace(",", "") + '_' +
                               str(characteristic['Dimension']).replace(" ", "").replace(",", "")+ '_' +
                               str(characteristic['Level']).replace(" ", "").replace(",", "")]
        characteristic_description = characteristic['Characteristic']
        characteristic_level = characteristic['Level']
        
        # characteristic triples

        graph.add((characteristic_uri, RDF.type, emm_ns.Characteristic))
        graph.add((characteristic_uri, SKOS.definition, Literal(characteristic_description)))
        graph.add((characteristic_uri, emm_ns.maturityScore, Literal(characteristic_level)))
        graph.add((characteristic_uri, DCTERMS.isPartOf, dimension_uri))
        graph.add((characteristic_uri, RDFS.isDefinedBy, URIRef(emm_ns)))
        graph.add((characteristic_uri, SKOS.prefLabel, Literal(characteristic_name, lang='en')))

        # dimension triples

        graph.add((dimension_uri, RDF.type, emm_ns.Dimension))
        graph.add((dimension_uri, DCTERMS.isPartOf, lvl2_uri))
        graph.add((dimension_uri, RDFS.isDefinedBy, URIRef(emm_ns)))
        graph.add((dimension_uri, SKOS.prefLabel, Literal(dimension_name, lang='en')))

        # lvl 2 capability tripples

        graph.add((lvl2_uri, RDF.type, emm_ns.Capability))
        graph.add((lvl2_uri, DCTERMS.isPartOf, lvl1_uri))
        graph.add((lvl2_uri, RDFS.isDefinedBy, URIRef(emm_ns)))
        graph.add((lvl2_uri, SKOS.prefLabel, Literal(lvl2_name, lang='en')))

        # lvl 1 capability tripples
        graph.add((lvl1_uri, RDF.type, emm_ns.Capability))
        graph.add((lvl1_uri, RDFS.isDefinedBy, URIRef(emm_ns)))
        graph.add((lvl1_uri, SKOS.prefLabel, Literal(lvl1_name, lang='en')))

    graph.serialize(destination= output_rdf)      

    return graph


