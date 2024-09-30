"""
This file supports Inventory Pattern for plascode
"""

from datetime import datetime, timedelta
import random
import uuid
from dateutil.parser import parse

from typing import Union, List, Tuple, Dict
from typing_extensions import Annotated


from syncmodels.model import BaseModel, field_validator, Field
from syncmodels.mapper import *

# from models.generic.price import PriceSpecification
# from models.generic.schedules import OpeningHoursSpecificationSpec

from plascode.definitions import UID_TYPE

from .base import *
from ..ports import *

# TODO: extend model corpus classes, a.k.a: the pydantic based thesaurus foundations classes
# TODO: this classes may be included in the main thesaurus when project is stable
# TODO: and others projects can benefit from them, making the thesaurus bigger and more powerful

# ---------------------------------------------------------
# InventoryItem
# ---------------------------------------------------------
# TODO: Inherit from smartmodels.model.inventory (or similar) 
class PlascodeItem(Item):
    """A Plascode InventoryItem model"""
    pass

    
class PlascodeInventory(Item):
    """A Plascode InventoryItem model"""
    item: Dict[UID_TYPE, PlascodeItem] = {}


# ---------------------------------------------------------
# InventoryRequest
# ---------------------------------------------------------
class PlascodeInventoryRequest(Request):
    
    """A Plascode request to inventory manager.
    Contains all query data and search parameters.
    """
    pass
# ---------------------------------------------------------
# InventoryResponse
# ---------------------------------------------------------
class PlascodeInventoryResponse(Response):
    
    """A Plascode response to inventory manager.
    Contains the search results given by a request.
    """
    data: Dict[UID_TYPE, PlascodeItem] = {}







