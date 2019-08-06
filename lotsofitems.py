from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from catalog_db_setup import Base, User, Category, Item

# old engine:
# engine = create_engine('sqlite:///catalog3.db')
engine = create_engine('postgresql://catalog:fsnd@localhost/catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# delete from tables to initialize
num_rows_deleted = session.query(Category).delete()
session.commit()

num_rows_deleted = session.query(Item).delete()
session.commit()


golfCat = Category(name="Golf")
session.add(golfCat)
session.commit()

baseballCat = Category(name="Baseball")
session.add(baseballCat)
session.commit()

tennisCat = Category(name="Tennis")
session.add(tennisCat)
session.commit()

skiCat = Category(name="Downhill Skiing")
session.add(skiCat)
session.commit()

item1 = Item(name="Putter", description="A golf club used for \
    short shots on the green", category=golfCat)
session.add(item1)
session.commit()

item2 = Item(name="Pitching Wedge", description="A golf club used \
    for short shots that require loft", category=golfCat)
session.add(item2)
session.commit()

item3 = Item(
    name="Nine Iron",
    description="greatest loft and the shortest shaft",
    category=golfCat)
session.add(item3)
session.commit()

item4 = Item(
    name="Eight Iron",
    description="A golf club with a small head and an angled face. \
    As the number of the iron increases, the loft increases and the \
    length of the shaft decreases, making the eight iron intermediate",
    category=golfCat)
session.add(item4)
session.commit()

item5 = Item(
    name="Seven Iron",
    description="A golf club with a small head and an angled face.  \
    As the number of the iron increases, the loft increases and the \
    length of the shaft decreases, making the seven iron intermediate",
    category=golfCat)
session.add(item5)
session.commit()

item6 = Item(
    name="Six Iron",
    description="A golf club with a small head and an angled face.  \
    As the number of the iron increases, the loft increases and the \
    length of the shaft decreases, making the six iron intermediate",
    category=golfCat)
session.add(item6)
session.commit()

item7 = Item(
    name="Five Iron",
    description="A golf club with a small head and an angled face.  \
    As the number of the iron increases, the loft increases and the \
    length of the shaft decreases, making the five iron intermediate",
    category=golfCat)
session.add(item7)
session.commit()

item8 = Item(
    name="Four Iron",
    description="A golf club with a small head and an angled face.  \
    As the number of the iron increases, the loft increases and the \
    length of the shaft decreases, making the four iron intermediate",
    category=golfCat)
session.add(item8)
session.commit()

item9 = Item(
    name="Three Iron",
    description="A golf club with a small head and an angled face.  \
    The three iron has the smallest loft and the longest shaft relative \
    to other irons",
    category=golfCat)
session.add(item8)
session.commit()

print "A few items added, categories Golf, Baseball, Tennis, Downhill Skiing"
