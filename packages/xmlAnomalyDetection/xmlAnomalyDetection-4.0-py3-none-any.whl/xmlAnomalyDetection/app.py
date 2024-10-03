from fastapi import FastAPI, File, UploadFile

from pydantic import BaseModel
import xml.etree.ElementTree as ET
from langchain.output_parsers.openai_tools import PydanticToolsParser
from pydantic import BaseModel as BaseModelPydantic
from langchain.pydantic_v1 import BaseModel, Field
from typing import Optional, List
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import uvicorn
import json
import os
from xmlAnomalyDetection.parsers import ParserApplier

os.environ['GROQ_API_KEY']='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'

app = FastAPI()


class XMLData(BaseModelPydantic):
    xml_string: str


class anomaly_parser(BaseModel):
    user_entered_values: Optional[List[str]] = Field(None, description="The values that have been filled by user")
    entered_values_decriptions: Optional[List[str]] = Field(None,
                                                            description="the description of the fields  in the same order as user_entered_values , if there is no description then '' ")
    is_anomaly: Optional[str] = Field(None,
                                      description="decision, if there is anomaly it should be True else it should be False")
    reason: Optional[List[str]] = Field(None, description="List of reasons stating why is this marked as anomaly")



def all_parsers(xml_str):
    """
    apply all the parsers

    Parameters
    ----------
    xml_str : str
        string representation of xml

    Returns
    -------
    str
    """
    parser_applier = ParserApplier()
    result = parser_applier.apply_all_parsers(xml_str)
    return result

parser = PydanticToolsParser(tools=[anomaly_parser])
model = ChatGroq(model="llama-3.1-70b-versatile", temperature=0).bind_tools([anomaly_parser])

prompt = ChatPromptTemplate.from_messages(
    [("system", """
    You are expert at analyzing the given expense data filled by company employees, employees are filling data and they can be confident that they are not going to make mistakes. You need to find the user filled fields, and then on basis of the field and field type and description you need to detect the anomalies, if there is anomaly found then mark "is_anomaly" as True and also give the list of reasons why it is anomaly

    Here are some examples:


    | Field Type | Field Description | User Entered Value | |------------|------------------|---------------------| | Date | Date of expense | 2022-12-31 | | Category | Type of expense | Food | | Amount | Expense amount | 200.00 | | Description| Brief description| Lunch with clients |

| Field Type | Field Description | User Entered Value | |------------|------------------|---------------------| | Date | Date of expense | 2023-02-01 | | Category | Type of expense | Transportation | | Amount | Expense amount | 5000.00 | | Description| Brief description| Flight to NY |

| Field Type | Field Description | User Entered Value | |------------|------------------|---------------------| | Date | Date of expense | 2022-12-35 | | Category | Type of expense | Hotel | | Amount | Expense amount | 800.00 | | Description| Brief description| Stay at Hilton |

Anomalous value: Date is invalid

| Field Type | Field Description | User Entered Value | |------------|------------------|---------------------| | Date | Date of expense | 2023-01-15 | | Category | Type of expense | Miscellaneous | | Amount | Expense amount | 100000.00 | | Description| Brief description| Gift for friend |

Anomalous value: Amount is unusually high

| Field Type | Field Description | User Entered Value | |------------|------------------|---------------------| | Date | Date of expense | 2022-12-20 | | Category | Type of expense | Entertainment | | Amount | Expense amount | 50.00 | | Description| Brief description| Dinner with family |

| Field Type | Field Description | User Entered Value | |------------|------------------|---------------------| | Date | Date of expense | 2023-03-01 | | Category | Type of expense | Office Supplies | | Amount | Expense amount | 10000.00 | | Description| Brief description| Purchased chairs |

Anomalous value: Amount is unusually high for office supplies

| Field Type | Field Description | User Entered Value | |------------|------------------|---------------------| | Date | Date of expense | 2022-11-30 | | Category | Type of expense | Travel | | Amount | Expense amount | 200.00 | | Description| Brief description| Cab fare |

| Field Type | Field Description | User Entered Value | |------------|------------------|---------------------| | Date | Date of expense | 2023-01-31 | | Category | Type of expense | Education | | Amount | Expense amount | 500.00 | | Description| Brief description| Online courses |

| Field Type | Field Description | User Entered Value | |------------|------------------|---------------------| | Date | Date of expense | 2022-12-32 | | Category | Type of expense | Networking | | Amount | Expense amount | 150.00 | | Description| Brief description| Conference attendance|

Anomalous value: Date is invalid

| Field Type | Field Description | User Entered Value | |------------|------------------|---------------------| | Date | Date of expense | 2023-02-28 | | Category | Type of expense | Software | | Amount | Expense amount | 2000.00 | | Description| Brief description| Adobe subscription |

    Your answer should be a simple True/False and a list of reasons why its anomaly, and the fields filled by user


    """),

     ("user", "Here is the single long form that user entered:\n{xml_extracted}")]
)

chain = prompt | model | parser

@app.post("/detect_anomaly")
async def detect_anomaly(xml_file: UploadFile = File(...)):
    xml_string = await xml_file.read()
    xml_string = xml_string.decode("utf-8")  # Specify the correct encoding here
    #data_as_dict = extract_data_from_xml(xml_string)
    parsed_string = all_parsers(xml_string)
    #results = chain.invoke({"xml_extracted": json.dumps(data_as_dict)})
    results = chain.invoke({"xml_extracted": parsed_string})
    results = [k.__dict__ for k in results]
    return results
def runserver():
    uvicorn.run(app, host='0.0.0.0', port=8357, log_level="debug")
