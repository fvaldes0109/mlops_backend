from pydantic import BaseModel
from typing import Optional, List

class ChatInput(BaseModel):
    prompt: str
    max_token_count: int

class CreditInput(BaseModel):
    Attribute1: str
    Attribute2: int
    Attribute3: str
    Attribute4: str
    Attribute5: int
    Attribute6: str
    Attribute7: str
    Attribute8: int
    Attribute9: str
    Attribute10: str
    Attribute11: int
    Attribute12: str
    Attribute13: int
    Attribute14: str
    Attribute15: str
    Attribute16: int
    Attribute17: str
    Attribute18: int
    Attribute19: str
    Attribute20: str

class AttributeValue(BaseModel):
    identifier: str
    name: str

class Attribute(BaseModel):
    name: str
    values: Optional[List[AttributeValue]] = None  # None means it's a numerical attribute

# Define the attributes
attributes = [
    Attribute(
        name="Status of existing checking account",
        values=[
            {"identifier": "A11", "name": "... < 0 DM"},
            {"identifier": "A12", "name": "0 <= ... < 200 DM"},
            {"identifier": "A13", "name": "... >= 200 DM / salary assignments for at least 1 year"},
            {"identifier": "A14", "name": "no checking account"},
        ]
    ),
    Attribute(name="Duration in month"),  # numerical
    Attribute(
        name="Credit history",
        values=[
            {"identifier": "A30", "name": "no credits taken/ all credits paid back duly"},
            {"identifier": "A31", "name": "all credits at this bank paid back duly"},
            {"identifier": "A32", "name": "existing credits paid back duly till now"},
            {"identifier": "A33", "name": "delay in paying off in the past"},
            {"identifier": "A34", "name": "critical account/ other credits existing (not at this bank)"},
        ]
    ),
    Attribute(
        name="Purpose",
        values=[
            {"identifier": "A40", "name": "car (new)"},
            {"identifier": "A41", "name": "car (used)"},
            {"identifier": "A42", "name": "furniture/equipment"},
            {"identifier": "A43", "name": "radio/television"},
            {"identifier": "A44", "name": "domestic appliances"},
            {"identifier": "A45", "name": "repairs"},
            {"identifier": "A46", "name": "education"},
            {"identifier": "A47", "name": "(vacation - does not exist?)"},
            {"identifier": "A48", "name": "retraining"},
            {"identifier": "A49", "name": "business"},
            {"identifier": "A410", "name": "others"},
        ]
    ),
    Attribute(name="Credit amount"),  # numerical
    Attribute(
        name="Savings account/bonds",
        values=[
            {"identifier": "A61", "name": "... < 100 DM"},
            {"identifier": "A62", "name": "100 <= ... < 500 DM"},
            {"identifier": "A63", "name": "500 <= ... < 1000 DM"},
            {"identifier": "A64", "name": ".. >= 1000 DM"},
            {"identifier": "A65", "name": "unknown/ no savings account"},
        ]
    ),
    Attribute(
        name="Present employment since",
        values=[
            {"identifier": "A71", "name": "unemployed"},
            {"identifier": "A72", "name": "... < 1 year"},
            {"identifier": "A73", "name": "1 <= ... < 4 years"},
            {"identifier": "A74", "name": "4 <= ... < 7 years"},
            {"identifier": "A75", "name": ".. >= 7 years"},
        ]
    ),
    Attribute(name="Installment rate in percentage of disposable income"),
    Attribute(
        name="Personal status and sex",
        values=[
            {"identifier": "A91", "name": "male : divorced/separated"},
            {"identifier": "A92", "name": "female : divorced/separated/married"},
            {"identifier": "A93", "name": "male : single"},
            {"identifier": "A94", "name": "male : married/widowed"},
            {"identifier": "A95", "name": "female : single"},
        ]
    ),
    Attribute(
        name="Other debtors / guarantors",
        values=[
            {"identifier": "A101", "name": "none"},
            {"identifier": "A102", "name": "co-applicant"},
            {"identifier": "A103", "name": "guarantor"},
        ]
    ),
    Attribute(name="Present residence since"),
    Attribute(
        name="Property",
        values=[
            {"identifier": "A121", "name": "real estate"},
            {"identifier": "A122", "name": "building society savings/life insurance"},
            {"identifier": "A123", "name": "car or other, not in attribute 6"},
            {"identifier": "A124", "name": "unknown / no property"},
        ]
    ),
    Attribute(name="Age in years"),
    Attribute(
        name="Other installment plans",
        values=[
            {"identifier": "A141", "name": "bank"},
            {"identifier": "A142", "name": "stores"},
            {"identifier": "A143", "name": "none"},
        ]
    ),
    Attribute(
        name="Housing",
        values=[
            {"identifier": "A151", "name": "rent"},
            {"identifier": "A152", "name": "own"},
            {"identifier": "A153", "name": "for free"},
        ]
    ),
    Attribute(name="Number of existing credits at this bank"),
    Attribute(
        name="Job",
        values=[
            {"identifier": "A171", "name": "unemployed/ unskilled - non-resident"},
            {"identifier": "A172", "name": "unskilled - resident"},
            {"identifier": "A173", "name": "skilled employee / official"},
            {"identifier": "A174", "name": "management/ self-employed/ highly qualified employee/ officer"},
        ]
    ),
    Attribute(name="Number of people being liable to provide maintenance for"),
    Attribute(
        name="Telephone",
        values=[
            {"identifier": "A191", "name": "none"},
            {"identifier": "A192", "name": "yes, registered under the customer's name"},
        ]
    ),
    Attribute(
        name="foreign worker",
        values=[
            {"identifier": "A201", "name": "yes"},
            {"identifier": "A202", "name": "no"},
        ]
    ),
]

def get_attributes():
    return attributes