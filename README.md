# Flask Factor

*Evan Young February 2021*

## Summary
Flack Factor is a treasure management system for Pathfinder RPG, it attempts to provide a place to collect treasure that our adventuring company collects, value it and distribute it. It could be given to a company member, stored, or sold by our 'Factor' a kind of merchant. The money earned from sales is returned to the company and can be distributed to the members of the company with an option for a percentage to be held in the company 'account'.

Note, this is a readme, yes, but it's also an account of my 'run' with getting this developed so take that as you might.

## Note
This is a Python / Flask / SQLite etc. learning project for me so please don't use this as a good example of programming, still very much learning this stack.

**20 Feb 21**
Returning to this after a bit away on my CoinPurse project, need to re-factor a bunch to match that structure better.

**20 Mar 21**
Got the docker config one of my other projects working coming back to this one now.

**28 Mar 21**
Alright, much success I have the docker and docker-compose running as well as nginx and gunicorn. Also the home page and most of the Character and Player page, Party has an add but not yet an edit. Login, Sign-Up and logout all work so that also good. When I was working on the docker setup it was throwing some routing / path errors when I was moving around need to review and see if I can fix those up. I'm now thinking of deployment on Heroku rather than Google, the potential of some kind of run-away billing is frankly frightening.

**29 Mar 21**
Finished up the Refactor of Character Edit and adding Party Edit!

**25 Sept 22**
Well, picking this up after a (very) long time... Adding the receiving form and it's tests. I want to do some work in the tests with mocking.

**25 Feb 23**
Added configuration for black formatter to the app.
I've been learning mocking and patching for tests, I'll try adding some more proper test. Added the MIT Licence File

**26 Feb 23**
Doing some reading around the testing I'm setting up. Perhaps my 'in memory' testing is just fine, it is certainly less hassle than the mocking route.
I've reverted my mocking changes, added a `conftest` file and I'm setting up the tests to use a single shared app profile.

