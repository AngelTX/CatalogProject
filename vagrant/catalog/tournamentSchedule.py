from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Game, Tournament

engine = create_engine('sqlite:///upcomingTournaments.db')
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

#**************Tournaments for League of Legends*****************
game1 = Game(name="League of Legends")
session.add(game1)
session.commit()

tourny1 = Tournament(name='Mid-Season Invitational 2018',
            description="At MSI 2018, 14 teams participate across multiple stages.",
            location="Berlin & Paris",
            startDate="May 3, 2018",
            endDate="May 21, 2018",
            game=game1)
session.add(tourny1)
session.commit()

tourny2 = Tournament(name='2018 EU Masters - Main Event',
            description="Heading to the The Haymarket Theatre in Leicester UK, teams from all over Europe will be competing to establish themselves and their home-ERL as the dominant force in the region, a share of the 150,000 EUR prize pool and, most importantly, EU-wide bragging rights valid at least until the next European Masters tournament.",
            location="Online, Europe",
            startDate="April 9, 2018",
            endDate="April 12, 2018",
            game=game1)
session.add(tourny2)
session.commit()

tourny3 = Tournament(name='2018 EU Masters - Play-in',
            description="Heading to the The Haymarket Theatre in Leicester UK, teams from all over Europe will be competing to establish themselves and their home-ERL as the dominant force in the region, a share of the 150,000 EUR prize pool and, most importantly, EU-wide bragging rights valid at least until the next European Masters tournament.",
            location="Online, Europe",
            startDate="April 9, 2018",
            endDate="April 12, 2018",
            game=game1)
session.add(tourny3)
session.commit()

tourny4 = Tournament(name='2018 NA LCS Spring Split',
            description="The 2018 NA League Championship Series is the sixth season of North America's fully professional League of Legends league. Ten teams will compete in a round robin group stage, with the top 6 teams continuing to playoffs.",
            location="Los Angeles",
            startDate="January 20, 2018",
            endDate="March 18, 2018",
            game=game1)
session.add(tourny4)
session.commit()

tourny5 = Tournament(name='2018 NA LCS Regional Qualifier',
            description="The 2017 NA LCS Regional Qualifier will determine the last team (3rd seed) that will represent the North American Region in the 2017 World Championship",
            location="Los Angeles",
            startDate="September 8, 2017",
            endDate="September 10, 2017 ",
            game=game1)
session.add(tourny5)
session.commit()

#*******************Tournament for Overwatch****************
game2 = Game(name="Overwatch")
session.add(game2)
session.commit()

tourny1 = Tournament(name="Overwatch mini Tournament",
            description="This Tournament is for amateurs to high ranks, looking for some practice, some fun and most importantly some winning!",
            location="Online, hyderabad",
            startDate="April 24, 2018",
            endDate="April 27, 2018",
            game=game2)
session.add(tourny1)
session.commit()

tourny2 = Tournament(name="Overwatch Uprising League",
            description="The Uprising Community is a place for people of all ages and skill to compete in a League-style tournament.",
            location="Online",
            startDate="May 21, 2018",
            endDate="December 21, 2018",
            game=game2)
session.add(tourny2)
session.commit()

tourny3 = Tournament(name="League of Ladies Overwatch Tournament",
            description="Female Legends is a community for females that plays e-sport. Whether you play to climb or just want to find other female gamers to have fun with, FL is for you",
            location="Online",
            startDate="June 3, 2018",
            endDate="June 3, 2018",
            game=game2)
session.add(tourny3)
session.commit()

tourny4 = Tournament(name="Overwatch Tranquility Community",
            description="The Overwatch Tranquility Community is a casual league to enjoy the game and time with friends. While it is intended to be a competitive league; its spirit is of friendly competition.",
            location="Online, North America",
            startDate="June 20, 2018",
            endDate="September 29, 2018",
            game=game2)
session.add(tourny4)
session.commit()

tourny5 = Tournament(name="Rapture Gaming Festival Tour: Colchester - Overwatch 3v3 Open",
            description="Welcome to the RGF Esports Experience! We aim to provide a tournament experience, with focus on fun, competition & introducing players to the Esports world.",
            location="Charter Hall, Colchester",
            startDate="July 21, 2018",
            endDate="July 21, 2018",
            game=game2)
session.add(tourny5)
session.commit()

#**********************Tournament for Fortnite****************************
game3 = Game(name="Fortnite")
session.add(game3)
session.commit()

tourny1 = Tournament(name="Friendly Royale",
            description="Casual amature match.",
            location="Los Angeles",
            startDate="May 3, 2018",
            endDate="May 6, 2018",
            game=game3)
session.add(tourny1)
session.commit()

tourny2 = Tournament(name="NA Clash",
            description="Top teams in NA battle it out",
            location="New York",
            startDate="June 25, 2018",
            endDate="June 30, 2018",
            game=game3)
session.add(tourny2)
session.commit()

tourny3 = Tournament(name="Dreamhack",
            description="Invitational inviting top teams around the world in a best of 5 skirmish.",
            location="Los Angeles",
            startDate="September 3, 2018",
            endDate="September 6, 2018",
            game=game3)
session.add(tourny3)
session.commit()

tourny4 = Tournament(name="Pre-Worlds Invitational",
            description="Qualifying round for worlds.",
            location="Seoul, South Korea",
            startDate="October 16, 2018",
            endDate="October 20, 2018",
            game=game3)
session.add(tourny4)
session.commit()

tourny5 = Tournament(name="Worlds",
            description="Teams around the world compete to take the ultimate title and bring honour to their country.",
            location="London, UK",
            startDate="December 3, 2018",
            endDate="December 5, 2018",
            game=game3)
session.add(tourny5)
session.commit()

#*******************Tournaments for Melee*******************************
game4 = Game(name="Super Smash Bros. Melee")
session.add(game4)
session.commit()

tourny1 = Tournament(name="Let's Smash, Bros",
            description="Casual one night stand for a prize pool of $500. Lyft ride home not included.",
            location="Dallas, Tx",
            startDate="February 14, 2018",
            endDate="February 14, 2018",
            game=game4)
session.add(tourny1)
session.commit()

tourny2 = Tournament(name="GameInformer's skirmish",
            description="Promotional skirmishing featuring the staff of Game Informer",
            location="Los Angeles",
            startDate="May 6, 2018",
            endDate="May 6, 2018",
            game=game4)
session.add(tourny2)
session.commit()

tourny3 = Tournament(name="Global Pre-Qualifier EU",
            description="Players accross Europe battle it out for a shot at representing their country on the world stage.",
            location="Edingburg",
            startDate="July 13, 2018",
            endDate="July 16, 2018",
            game=game4)
session.add(tourny3)
session.commit()

tourny4 = Tournament(name="Global Pre-Qualifier NA",
            description="Players accross North America battle it out for a shot at representing their country on the world state.",
            location="New York",
            startDate="August 6, 2018",
            endDate=" August 9, 2018",
            game=game4)
session.add(tourny4)
session.commit()

tourny5 = Tournament(name="Global Brawl",
            description="Players across the world battle it out in an all out war for global domination.",
            location="International Space Station",
            startDate="December 25, 2018",
            endDate="December 31, 2018",
            game=game4)
session.add(tourny5)
session.commit()

print "all tournys added!"
