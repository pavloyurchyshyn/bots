from core.mech.details.detail import BaseDetail
from core.mech.details.constants import *


class BaseLeg(BaseDetail):
    is_limb = True
    detail_type = DetailsTypes.LEG_TYPE

    def __init__(self, unique_id, **kwargs):
        super().__init__(unique_id=unique_id, **kwargs)
