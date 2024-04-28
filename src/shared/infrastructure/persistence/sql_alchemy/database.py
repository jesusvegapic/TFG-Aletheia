import logging
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import force_auto_coercion

logger = logging.getLogger(__name__)

force_auto_coercion()
Base = declarative_base()
