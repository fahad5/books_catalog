from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy_utils import database_exists, drop_database, create_database

from database_setup import Category, Books, User, Base

engine = create_engine('sqlite:///itemcatalog.db')

# Clear database
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user
user1 = User(name="Fahad Abdullah", email="Fahad@udacity.com",
             picture='https://img.icons8.com/color/96/000000/administrator-male.png')
session.add(user1)
session.commit()

# Items for Strings
category1 = Category(name="Action & Adventure ", user_id=1)

session.add(category1)
session.commit()

item1 = Books(name="Harry Potter", user_id=1, description="Harry Potter has never even heard of Hogwarts when the letters start dropping on the doormat at number four, Privet Drive."+  \
 " Addressed in green ink on yellowish parchment with a purple seal, they ", category=category1)

session.add(item1)
session.commit()

item2 = Books(name="The Secret Of The Nagas ", user_id=1, description="The Shiva Trilogy, written by Amish Tripathi, has become a nation-wide bestseller in a short time. This is due to the"  +  \
	"refreshing new plot that it explores and the unique writing style of the author. The Secret of The Nagas is the second novel in the saga. Amish has penned down the contents of this book"+  \
	 "in such a way that it manages to shine as a stand-alone book in itself.", category=category1)

session.add(item2)
session.commit()

item3 = Books(name="Sita: Warrior of Mithila", user_id=1, description="Immerse yourself in book 2 of the Ram Chandra series, based on the Ramayana, the story of Lady Sita, written by the multi-million" +  \
 "bestselling Indian Author Amish; the author who has transformed Indian Fiction with his unique combination of mystery, mythology, religious symbolism and philosophy. In this book, you will follow Lady Sita's" +  \
 "journey from an Adopted Child to the Prime Minister to finding her true calling. You will find all the familiar characters you have heard of, like Lord Ram and Lord Lakshman and see more of Lord Hanuman and many" +  \
 "others from Mithila. You will also start discovering the true purpose of the Vayuputras and Malayaputras and their conflicting ideologies that leads to plot twists, politics and intrigue as they try to influence" +  \
 "outcomes from behind the scenes.", category=category1)

session.add(item3)
session.commit()

# Items for Woodwinds
category2 = Category(name="Arts, Film & Photography", user_id=1)

session.add(category2)
session.commit()

item1 = Books(name="7 Secrets of Shiva", user_id=1, description="Shiva among the Hindu trinity (of gods), is depicted in many contradictory manners. He is an ascetic who wears animal skin, his body smeared" +  \
 "with ashes. Contradictory to his wild nature, he is also depicted as having a family, with a beautiful wife and two children. There are many more such varied representations of Shiva, the most prominent of" +  \
 "these being the Linga and the Nataraja. The author, Devdutt Pattanaik, introduces he readers to these varied aspects and representations, and then sets about interpreting them. He explains the different anomalies and conflicts in beliefs, as well as the symbolism, rituals and reasons behind Hindu worship.", category=category2)

session.add(item1)
session.commit()

item2 = Books(name="Lonely Planet's Beautiful World", user_id=1,  description="Journey to the planet's most magnificent places and see the world as you've never seen it before through the lenses of Lonely Planet," +  \
	"the world's leading travel guide publisher. Forty years of passion and experience has been poured into this thought-provoking portrait of our beautiful world. Inspired by our love of travel, this lavishly-produced," +  \
	"landmark pictorial, now available in paperback, shares more than 300 sublime photographs of the world's most captivating spectacles and will renew your relationship with the place we call home.", category=category2)

session.add(item2)
session.commit()

item3 = Books(name="Guitar: Fretboard Mastery", user_id=1, description="Unlock the Secrets of the Guitar Fretboard and Learn How to Massively Improve your Guitar Playing Skills with the Power of Understanding.", category=category2)

session.add(item3)
session.commit()

# Items for Percussion
category3 = Category(name="Design & Fashion", user_id=1)

session.add(category3)
session.commit()

item1 = Books(name="The Design of Everyday Things", user_id=1, description="Even the smartest among us can feel inept as we fail to figure out which light switch or oven burner to turn on, or whether to push, pull, or" +  \
	"slide a door. The fault, argues this ingenious-even liberating-book, lies not in ourselves, but in product design that ignores the needs of users and the principles of cognitive psychology. The problems range from" +  \
	"ambiguous and hidden controls to arbitrary relationships between controls and functions, coupled with a lack of feedback or other assistance and unreasonable demands on memorization.", category=category3)

session.add(item1)
session.commit()

item1 = Books(name="Design As Art", user_id=1, description="One of the last surviving members of the futurist generation, Bruno Munari's Design as Art is an illustrated journey into the artistic possibilities of modern" +  \
	"design translated by Patrick Creagh published as part of the 'Penguin on Design' series in Penguin Modern Classics. 'The designer of today re-establishes the long-lost contact between art and the public, between living people and art as a living thing' Bruno Munari was among the most inspirational designers of all time, described by Picasso as 'the new Leonardo'. Munari insisted that design be beautiful", category=category3)

session.add(item2)
session.commit()

item3 = Books(name="Universal Principles of Design", user_id=1, description="Universal Principles of Design, Revised and Updated is a comprehensive, cross-disciplinary encyclopedia covering 125 laws, guidelines, human"+  \
 "biases, and general considerations important to successful design. Richly illustrated and easy to navigate, it pairs clear explanations of every design concept with visual examples of the ideas applied in practice. From"+  \
  "the 80/20 Rule to the Weakest Link, every major design concept is defined and illustrated.", category=category3)

session.add(item3)
session.commit()

# Items for Brass
category4 = Category(name="Painting", user_id=1)

session.add(category4)
session.commit()


categories = session.query(Category).all()
for category in categories:
    print "Category: " + category.name