import statistics

from datetime import date, datetime, time, timedelta
from typing import List, Optional
from pydantic import BaseModel
from typing import Union


class MaturityScore(BaseModel) :
    resultTime : Optional[datetime] = None
    # raw_data : List[Union[str, int]]= []
    averageScore : Union[str, float]
    standardDeviation : Union[str, float]
    medianScore : Union[str, float]
    modeScore : Union[str, float]
    totalAnswers : int
    numberOfUnsure : int
    # unknown means the answer that was given was not recognized as one of the multiple choice answers, 
    # this indicates a problem with the data collection process or the data interpretation process 
    # in the sense that they are not alligned
    numberOfUnknown : int 


def raw_data_to_MaturityScore( raw_data : list):
    numericValues= [elm for elm in raw_data if isinstance(elm, int)]

    if len(numericValues) > 1 :
                    averageScore= statistics.mean(numericValues)
                    standardDeviation= statistics.pstdev(numericValues)
                    medianScore= statistics.median(numericValues)
                    modeScore= statistics.mode(numericValues)
    elif len(numericValues) == 1 :
                    averageScore= numericValues[0]
                    standardDeviation= 'Not Enough Data'
                    medianScore= numericValues[0]
                    modeScore= numericValues[0]
    else :
                    averageScore= 'Not Enough Data'
                    standardDeviation= 'Not Enough Data'
                    medianScore= 'Not Enough Data'
                    modeScore= 'Not Enough Data'

    numberOfUnsure = len([elm for elm in raw_data if elm =='Unsure'])
    numberOfUnknown = len([elm for elm in raw_data if elm =='Unknown'])

    tempmaturityScore = MaturityScore(
                    raw_data = raw_data,
                    averageScore= averageScore,
                    standardDeviation= standardDeviation,
                    medianScore= medianScore,
                    modeScore= modeScore,
                    totalAnswers= len(raw_data),
                    numberOfUnsure= numberOfUnsure,
                    numberOfUnknown= numberOfUnknown
                )
    
    return tempmaturityScore