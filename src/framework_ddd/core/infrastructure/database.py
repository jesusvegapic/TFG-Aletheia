from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import force_auto_coercion  # type: ignore

force_auto_coercion()
Base = declarative_base()
