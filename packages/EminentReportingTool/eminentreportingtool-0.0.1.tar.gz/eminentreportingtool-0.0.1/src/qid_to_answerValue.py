def qid_to_answerValue(AS, root,  target_qid): 

    # AS= the answerset within the xml tree
    # root= the whole tree
    # target_qid = the question id for which we would like to parse the answer

    qid_to_aid = {} 
    for answer in AS.findall(".//Answer"):
        qid = answer.get("qid")
        aid = answer.get("aid")
        qid_to_aid.setdefault(qid, []).append(aid) 


    # Retrieve the corresponding aid
    if target_qid in qid_to_aid:
        target_aid = qid_to_aid[target_qid]

        value = []
        for taid in target_aid :
        # Now find the corresponding value in the Survey section
            for survey_answer in root.findall(".//Survey/Elements/Answer[@id='{}']".format(taid)):
                
                value.append(survey_answer.text)
                #print(f"Value for qid '{target_qid}': {value}")

        return value
    else:
        print(f"No value found for qid '{target_qid}' in the survey.")
        return []
