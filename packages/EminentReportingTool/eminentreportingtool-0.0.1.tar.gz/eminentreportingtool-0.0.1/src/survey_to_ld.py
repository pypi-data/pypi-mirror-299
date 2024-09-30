import xml.etree.ElementTree as ET
import xml.etree.ElementTree as ET
from rdflib import Graph, Namespace, URIRef, Literal, BNode
from rdflib.namespace import FOAF, DCTERMS, DCAT, PROV, OWL, RDFS, RDF, XMLNS, SKOS, SOSA, ORG, SSN

from pydantic import BaseModel
import classify_characteristic



class Dimension(BaseModel) :
    id : str
    label : str

def survey_to_rdf(input_xml = str, version_number= str, output_rdf= str, serialization = 'ttl') :
    # Read the XML content from a file
    with open(input_xml, "r") as file:
        xml_content = file.read()
    # Parse the XML content
    root = ET.fromstring(xml_content)

    graph = Graph()
    emar_ns= Namespace("http://eminent.intnet.eu/maturity_assessment_results#")
    ema_ns = Namespace("http://eminent.intnet.eu/maturity_assessment#")
    emm_ns = Namespace("http://eminent.intnet.eu/maturity_model#")
    sgam_ns = Namespace("http://eminent.intnet.eu/sgam#")
    graph.bind("emar", emar_ns)
    graph.bind("ema", ema_ns)
    graph.bind("emm", emm_ns)
    graph.bind("sgam", sgam_ns)

    graph.add((ema_ns.Unsure, SKOS.definition, Literal("Default response that should be given when the respondent does not know the answer to a question")))
    graph.add((ema_ns.Unsure, emm_ns.maturityScore, Literal('Unsure')))

    # these are questiona about the respondent, these should be ignored for this function as they are metadata and
    # handled separately
    whoAreYouQuestionIDs = [
        "a086bcf9-c9c9-8b58-a15a-0ab224d76de3",
        "0eb59ebe-5ffe-f965-78ca-852a40dc5ad7",
        "51194433-574f-111a-7b94-7f048ef4dd79",
        "0de32b34-c527-19d4-f6ca-76af0cd7b88b",
        "91cc8bfe-ee6e-c7e9-3462-b49021778bdc",
        "17d78fb6-586e-21f1-a958-93af40ed9c88",
        "9666d660-00fd-1a81-d1f7-717d39c6f5d7",
        "6d4606c8-31b7-5c8f-4463-5be353ea4f64",
        "b1acefb8-c977-c91a-b82c-6bee6a82a34d",
        "32457cf6-2f78-5a25-7691-cad210b83222", 
        "384d5d53-9820-c0d1-a1cb-e6960e158527"
    ]

    question_identifier_to_uri = {
        '1.1.i': 'http://eminent.intnet.eu/maturity_model#CommunityGrowth_Information',
        '1.1.o': 'http://eminent.intnet.eu/maturity_model#CommunityGrowth_peopleandorganization',
        '1.1.p': 'http://eminent.intnet.eu/maturity_model#CommunityGrowth_process',
        '1.1.r': 'http://eminent.intnet.eu/maturity_model#CommunityGrowth_resources',
        '2.3.i': 'http://eminent.intnet.eu/maturity_model#ComplianceTesting_Information',
        '2.3.o': 'http://eminent.intnet.eu/maturity_model#ComplianceTesting_peopleandorganization',
        '2.3.p': 'http://eminent.intnet.eu/maturity_model#ComplianceTesting_process',
        '2.3.r': 'http://eminent.intnet.eu/maturity_model#ComplianceTesting_resources',
        '1.3.i': 'http://eminent.intnet.eu/maturity_model#DiversityofPerspectives_Information',
        '1.3.o': 'http://eminent.intnet.eu/maturity_model#DiversityofPerspectives_peopleandorganization',
        '1.3.p': 'http://eminent.intnet.eu/maturity_model#DiversityofPerspectives_process',
        '1.3.r': 'http://eminent.intnet.eu/maturity_model#DiversityofPerspectives_resources',
        '2.1.i': 'http://eminent.intnet.eu/maturity_model#IntegrationProfileEstablishment_Information',
        '2.1.o': 'http://eminent.intnet.eu/maturity_model#IntegrationProfileEstablishment_peopleandorganization',
        '2.1.p': 'http://eminent.intnet.eu/maturity_model#IntegrationProfileEstablishment_process',
        '2.1.r': 'http://eminent.intnet.eu/maturity_model#IntegrationProfileEstablishment_resources',
        '1.2.i': 'http://eminent.intnet.eu/maturity_model#KnowledgeRetention_Information',
        '1.2.o': 'http://eminent.intnet.eu/maturity_model#KnowledgeRetention_peopleandorganization',
        '1.2.p': 'http://eminent.intnet.eu/maturity_model#KnowledgeRetention_process',
        '1.2.r': 'http://eminent.intnet.eu/maturity_model#KnowledgeRetention_resources',
        '3.4.i': 'http://eminent.intnet.eu/maturity_model#MarketCreation_Information',
        '3.4.o': 'http://eminent.intnet.eu/maturity_model#MarketCreation_peopleandorganization',
        '3.4.p': 'http://eminent.intnet.eu/maturity_model#MarketCreation_process',
        '3.4.r': 'http://eminent.intnet.eu/maturity_model#MarketCreation_resources',
        '3.2.i': 'http://eminent.intnet.eu/maturity_model#OperationalAlignment_Information',
        '3.2.o': 'http://eminent.intnet.eu/maturity_model#OperationalAlignment_peopleandorganization',
        '3.2.p': 'http://eminent.intnet.eu/maturity_model#OperationalAlignment_process',
        '3.2.r': 'http://eminent.intnet.eu/maturity_model#OperationalAlignment_resources',
        '2.2.i': 'http://eminent.intnet.eu/maturity_model#Standardization_Information',
        '2.2.o': 'http://eminent.intnet.eu/maturity_model#Standardization_peopleandorganization',
        '2.2.p': 'http://eminent.intnet.eu/maturity_model#Standardization_process',
        '2.2.r': 'http://eminent.intnet.eu/maturity_model#Standardization_resources',
        '3.3.i': 'http://eminent.intnet.eu/maturity_model#ToolProductandReferenceImplementationDevelopment_Information',
        '3.3.o': 'http://eminent.intnet.eu/maturity_model#ToolProductandReferenceImplementationDevelopment_peopleandorganization',
        '3.3.p': 'http://eminent.intnet.eu/maturity_model#ToolProductandReferenceImplementationDevelopment_process',
        '3.3.r': 'http://eminent.intnet.eu/maturity_model#ToolProductandReferenceImplementationDevelopment_resources',
        '3.1.i': 'http://eminent.intnet.eu/maturity_model#UserBaseGrowth_Information',
        '3.1.o': 'http://eminent.intnet.eu/maturity_model#UserBaseGrowth_peopleandorganization',
        '3.1.p': 'http://eminent.intnet.eu/maturity_model#UserBaseGrowth_process',
        '3.1.r': 'http://eminent.intnet.eu/maturity_model#UserBaseGrowth_resources',
    }

    # instantiate questionnaireversion objects, it is assumed they are all versions of Eminent
    surveys= root.findall(".//Survey")
    for s in surveys :
        survey_uid = s.get('uid') # uuid of the survey
        survey_uri = ema_ns[survey_uid]
        survey_id = s.get('id') # eusurvey;s internal ID for the survey
        survey_name = s.get('alias') # the name of the survey
        graph.add((survey_uri, RDF.type, ema_ns.QuestionnaireVersion))
        graph.add((survey_uri, SKOS.prefLabel, Literal(survey_name)))
        graph.add((survey_uri, DCTERMS.identifier, Literal(survey_id)))
    # graph.add((survey_uri, DCAT.version, Literal('1.0.0')))
        graph.add((survey_uri, DCTERMS.isVersionOf, ema_ns.Eminent))
        # would prefer to use dcat:versionInfo but rdfLib is not up to dcat v3 and doesnt support it
        graph.add((survey_uri, OWL.versionInfo, Literal(version_number)))

        

        questions = s.findall(".//Question")

        for q in questions :
            if q.get('type') != 'Line' and q.get('id') not in whoAreYouQuestionIDs:
                question_id= q.get('id')
                question_uri = ema_ns[question_id]
                question_identifier = q.text[:5] # used for dcterms identifier
                question_phrasing = Literal(q.text, datatype=RDF.HTML)
                question_type = Literal(q.get('type'), lang='en')
                dimension_uri = URIRef(question_identifier_to_uri[question_identifier])

                graph.add((question_uri, RDF.type, ema_ns.Question))
                graph.add((question_uri, DCTERMS.identifier, Literal(question_identifier)))
                graph.add((question_uri, ema_ns.phrasing, Literal(question_phrasing)))
                graph.add((question_uri, DCTERMS.isPartOf, survey_uri))
                graph.add((question_uri, ema_ns.question_type, question_type))
                graph.add((question_uri, ema_ns.measures, dimension_uri))
                             

    graph.serialize(destination= output_rdf, format=serialization)

