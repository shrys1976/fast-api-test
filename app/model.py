from .database import Base
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, text
# creating the posts database
class Post(Base):
    __tablename__ ="posts"

    id = Column(Integer, primary_key=True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published  = Column(Boolean, server_default = text('true'), nullable = False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))


    # sqlalchemy doesnt let you modfiy already created tables
    # once the table with "name" has been created with the 
    # properties first set, even if u change the properties afterwards,
    # it will search for the table name and not modify the prop
    # to apply changes, manually delete the table and run code again







