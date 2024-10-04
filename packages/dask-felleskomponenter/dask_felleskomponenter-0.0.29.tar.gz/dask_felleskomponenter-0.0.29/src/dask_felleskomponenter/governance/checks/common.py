from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import requests

@dataclass(init=False)
class TableMetadata:
    catalog: Optional[str] = field(default=None)
    schema: Optional[str] = field(default=None)
    table: Optional[str] = field(default=None)
    beskrivelse: Optional[str] = field(default=None)
    tilgangsnivaa: Optional[str] = field(default=None)
    medaljongnivaa: Optional[str] = field(default=None)
    tema: Optional[str] = field(default=None)
    emneord: Optional[str] = field(default=None)
    epsg_koder: Optional[str] = field(default=None)
    begrep: Optional[str] = field(default=None)
    bruksvilkaar: Optional[str] = field(default=None)

    optional_params: Dict[str, Any] = field(default_factory=dict)

    def __init__(self, **kwargs):
        self.optional_params = {}
        for field_name in self.__dataclass_fields__:
            if field_name != 'optional_params':
                setattr(self, field_name, kwargs.get(field_name, None))
        for key, value in kwargs.items():
            if key not in self.__dataclass_fields__ and "delta." not in key:
                self.optional_params[key] = value

@dataclass
class MetadataError:
    catalog: str
    schema: str
    table: str
    column: Optional[str]
    description: str
    solution: Optional[str]
    for_field: str
    valid_values: str | List[str]

def get_valid_codelist_values(kodeliste_url: str, override_kodeliste_keyword: Optional[str] = None) -> List[str]:
    kodeliste_entry = "label" if override_kodeliste_keyword == None else override_kodeliste_keyword
    values_res = requests.get(kodeliste_url, headers={ "Accept": "application/json" }).json()
    valid_values = list(filter(lambda x: x != None, [x.get(kodeliste_entry, None) for x in values_res["containeditems"]]))
    return valid_values

def check_codelist_value(kodeliste_url: Optional[str], value: Any, allowed_values: Optional[List[Any]] = None, override_kodeliste_keyword: Optional[str] = None) -> bool:
    if value == None:
        return False

    if allowed_values != None:
        return value in allowed_values
    
    if kodeliste_url == None:
        return value != None

    valid_values = get_valid_codelist_values(kodeliste_url, override_kodeliste_keyword)
    return value in valid_values

if __name__ == "__main__":
    check_codelist_value("https://register.geonorge.no/api/register/sikkerhetsniva", "Ugradert", None, None)