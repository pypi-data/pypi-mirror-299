import xml.etree.ElementTree as ET
from rdflib import Graph, Namespace, URIRef, Literal, BNode
from rdflib.namespace import FOAF, DCTERMS, DCAT, PROV, OWL, RDFS, RDF, XMLNS, SKOS, SOSA, ORG
import hashlib
import classify_characteristic
import qid_to_answerValue


        
        
def answerset_to_rdf(input_xml = str, input_rdf=None , output_rdf= str, serialization= 'ttl' ):


    # Read the XML content from a file
    with open(input_xml, "r") as file:
        xml_content = file.read()
    # Parse the XML content
    root = ET.fromstring(xml_content)

    # if input_rdf is given, parse the graph and add the data from the xml to it, 
    # otherwise create a new graph
    # innitiate graph and all the namespaces
    graph = Graph()
    if input_rdf != None :
        graph.parse(input_rdf)   


    emar_ns= Namespace("http://eminent.intnet.eu/maturity_assessment_results#")
    ema_ns = Namespace("http://eminent.intnet.eu/maturity_assessment#")
    emm_ns = Namespace("http://eminent.intnet.eu/maturity_model#")
    sgam_ns = Namespace("http://eminent.intnet.eu/sgam#")
    graph.bind("emar", emar_ns)
    graph.bind("ema", ema_ns)
    graph.bind("emm", emm_ns)
    graph.bind("sgam", sgam_ns)

    AnswerSet = root.findall(".//AnswerSet")

    Survey_uid = root.findall("./Survey")[0].get('uid')
    Survey_uri = ema_ns[Survey_uid]

    # the following question ID's belong to questions in section 1 of the questionnaire and these 
    # are for the purpose of collecting metadata (not person identifyable) about the person who 
    # has given the response
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
    q1_id = whoAreYouQuestionIDs[0] # sgam domain area of expertise
    q2_id = whoAreYouQuestionIDs[1] # sgam zone area of expertise
    q3_id = whoAreYouQuestionIDs[2] # sgam layer area of expertise
    q4_id = whoAreYouQuestionIDs[3] # sgam layer area of expertise
    q5_id = whoAreYouQuestionIDs[4]
    q6_id = whoAreYouQuestionIDs[5]
    q7_id = whoAreYouQuestionIDs[6]
    q8_id = whoAreYouQuestionIDs[7]
    q9_id = whoAreYouQuestionIDs[8]
    q10_id = whoAreYouQuestionIDs[9] #study
    q6a_id = whoAreYouQuestionIDs[10] 
    # for each answerset in the xml file, create the rdf resource and add the relevant tripples
    for AS in AnswerSet:
        
        answerset_id = AS.get('list')
        print(answerset_id)
        print(len(AS))

        answerset_uri = emar_ns[answerset_id]
        # check if answerset has already been added to the graph
        if (len(AS) > 44) and ((answerset_uri, RDF.type, ema_ns.AnswerSet) not in graph) :


            # innitiate the person. organization, Area of Expertise and area of operation blanknodes
            person = BNode()
            organization = BNode()
            areaOfExpertise = BNode()
            areaOfOperation = BNode()

            # add tripples to graph to create basic structure for provenance information
            graph.add( (answerset_uri, PROV.wasQuotedFrom, person))
            graph.add((answerset_uri, SOSA.usedProcedure, Survey_uri))
            graph.add((person, RDF.type, FOAF.Person ))
            graph.add((person, PROV.actedOnBehalfOf, organization))
            graph.add((person, ema_ns.areaOfExpertise, areaOfExpertise))
            graph.add((organization, RDF.type, ORG.Organization))
            graph.add((organization, ema_ns.areaOfOperation, areaOfOperation))
            graph.add((areaOfExpertise, RDF.type, ema_ns.FocusArea))
            graph.add((areaOfOperation, RDF.type, ema_ns.FocusArea))

            # add informaton from q1-10 from questioonaire

            ## persons area of expertise
            dox= qid_to_answerValue.qid_to_answerValue(AS= AS, root=root, target_qid=q1_id)
            for i in dox:
                domainOfExpertise_uri = sgam_ns[str(i).replace(" ", "")]

                graph.add((areaOfExpertise, ema_ns.inDomain, domainOfExpertise_uri))

            zox = qid_to_answerValue.qid_to_answerValue(AS= AS, root=root, target_qid=q2_id)  
            for i in zox :
                zoneOfExpertise_uri = sgam_ns[str(i).replace(" ", "")]
                graph.add((areaOfExpertise, ema_ns.inZone, zoneOfExpertise_uri))

            lox = qid_to_answerValue.qid_to_answerValue(AS= AS, root=root, target_qid=q3_id)
            for i in lox :      
                layerOfExpertise_uri = sgam_ns[str(i).replace(" ", "")]
                graph.add((areaOfExpertise, ema_ns.onLayer , layerOfExpertise_uri))

            organizationDescription = qid_to_answerValue.qid_to_answerValue( AS=AS, root=root, target_qid= q4_id)
            for i in organizationDescription:
                graph.add((organization, ema_ns.description, Literal(i) ))

            orgsize = qid_to_answerValue.qid_to_answerValue( AS= AS, root=root, target_qid= q5_id)[0]
            graph.add((organization, ema_ns.organizationSize, Literal(orgsize)))

            sector = qid_to_answerValue.qid_to_answerValue(AS = AS, root=root, target_qid= q6_id)
            for i in sector:
                graph.add((organization, ema_ns.sector, Literal(i)))

            alt_sector = qid_to_answerValue.qid_to_answerValue(AS = AS, root=root, target_qid= q6a_id)
            if alt_sector != None:
                graph.add((organization, ema_ns.sector, Literal(alt_sector)))

            zoo = qid_to_answerValue.qid_to_answerValue(AS= AS, root=root, target_qid=q7_id)
            for i in zoo:
                zoneOfOperation_uri = sgam_ns[str(i).replace(" ", "")]
                graph.add((areaOfOperation, ema_ns.inZone, zoneOfOperation_uri))

            doo = qid_to_answerValue.qid_to_answerValue(AS= AS, root=root, target_qid=q8_id)
            for i in doo : 
                domainOfOperation_uri = sgam_ns[str(i).replace(" ", "")]
                graph.add((areaOfOperation, ema_ns.inDomain , domainOfOperation_uri))

            loo = qid_to_answerValue.qid_to_answerValue(AS= AS, root=root, target_qid=q9_id)
            for i in loo :
                layerOfOperation_uri = sgam_ns[str(i).replace(" ", "")]
                graph.add((areaOfOperation, ema_ns.onLayer, layerOfOperation_uri))

            # create the tripple that declares the type of the answerset
            graph.add((answerset_uri, 
                    URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), 
                    ema_ns.AnswerSet)
                    )
            Answers = AS.findall(".//Answer")

            studyIDs= AS.findall(".//Answer[@qid='{}']".format(q10_id))
            
            studyID= studyIDs[0].text.replace(" ", "")
            study_uri = emar_ns[studyID]

            graph.add((answerset_uri, DCTERMS.isPartOf, study_uri))

            ## itterate over the responded answers and add them to the graph
            for answer in Answers:
                question_id = answer.get("qid")
                
                if question_id not in whoAreYouQuestionIDs:

                    answer_id = answer.get('aid')

                    # In the source data, individual responses do not have a persistent ID that we can use to create a URI, 
                    # so we create a concatonation of aid, qid and answerset id to create seed for hash that will be part of the uri of the response
        
                    idseed= str(answerset_id + answer_id + question_id).encode('utf-8')
                    hash_obj = hashlib.sha1(idseed)
                    id_hash = hash_obj.hexdigest()
                    uniqueAnswerID =  str(id_hash)
                    answer_uri = emar_ns[uniqueAnswerID]
                    question_uri = ema_ns[question_id]
                    answer_value = str(qid_to_answerValue.qid_to_answerValue(AS=AS, root=root, target_qid=question_id )[0])
                    if answer_value != []:
                        if answer_value == "Unsure" or answer_value == "Unsure.": # nopt sure how we ever got a period there
                            choiceanswer_uri= ema_ns.Unsure
                        else :
                            # print(answer_value)
                            choiceanswer_uri = classify_characteristic.classify_characteristic(description=answer_value)
                            # print(choiceanswer_uri)


                    # add triples for each given answer to the graph
                        graph.add((answer_uri, SOSA.hasResult, choiceanswer_uri))
                        graph.add((answer_uri, ema_ns.resultText, Literal(answer_value)))
                        graph.add((answer_uri, RDF.type, ema_ns.Answer))
                        graph.add((answer_uri, DCTERMS.isPartOf, answerset_uri))
                    graph.add((answer_uri, SOSA.usedProcedure, question_uri))
                    



    #print(graph.serialize())
    graph.serialize(destination=output_rdf, format= serialization)

