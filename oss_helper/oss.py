import oss2

from config import oss_helper_cfs
from oss2 import Bucket


def get_bucket() -> Bucket:
    auth = oss2.Auth(oss_helper_cfs['oss']['access_key_id'], oss_helper_cfs['oss']['access_key_secret'])
    return oss2.Bucket(auth, oss_helper_cfs['oss']['endpoint'], oss_helper_cfs['oss']['bucket'])
