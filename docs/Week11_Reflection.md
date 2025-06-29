## Section 0: Fellow Details
GitHub Username: eclctc
Preferred Feature: Storing API calls with persistent storage to build data history, ML for prediction, Day/Night mode (easy implementation), and matplotlib for charting my ML data points
Team Interest:	Impartial. I'll be on one, but I really want to focus on the ML and data discovery piece of my project. So if I do end up on a team, I would really like to not have a technical role. I would be happy to work on design, owner/pm or tester though.

## Section 1: Week 11 Reflection
- Key Takeaways:
    - Overall I'm pretty comfortable with where I want to go with the project. I just need to start making decisions on exactly what features I want. I'm struggling with MVP and where I actually want to go with this.
    - It seems like a lot in a short period of time and it feels that a week per feature isn't going to be enough time. But I know when I get grinding that it will all start to flow more naturally.
    - I need to be more proactive in the planning portion of this. I really thought I was going to be able to just throw this together. But that is clearly not going to be the case.
    - I also really want to challenge myself this go around. Adding the machine learning piece is going to be my greatest challenge. Especially that we have to modularize it. I think I have a plan though!

## Section 2: Feature Selection Rationale
    - Feature 1: Basic prediction logic *** : I'm learning a lot about linear regression right now and I think I have the basic concepts down. So now it's time to implement. I just need to find the right data set to try.

    - Feature 2: Theme Switcher ** : I'm choosig this feature because it's a relatively easy implementation (already finished it locally, just need to break it out as a feature) and I want to have my bases covered to get the MVP ready to go.

    - Feature 3: Matplotlib embedded in Tkinter ** : I'm choosing this piece because it will go hand in hand with my machine learning implementation. My idea behind it is - show the data points, show the line, explain the correlation between the line and the points. I'll probably throw some more graphs in there too. But again, this piggy backs off of my ML implementation.

    - Enhancement: I'm still not 100% sure what I'm going to do with this yet. But I plan on tackling that problem this week.

##  Section 3: High-Level Architecture Sketch
    - See docs/sys_design.jpg

##  Section 4: Data Model Plan
    - Right now I have my data being saved to a csv file called weather_log in my root directory. The columns are formatted as follows:
        date, city, temperature, description, humidity, data_source
    I plan on moving the data collection/model into a relational database. I jsut need to find the right data set first.

##  Section 5: Personal Project Timeline (Weeks 12–17)
    - https://docs.google.com/spreadsheets/d/1q9gVPoGMUlMN1jJRhSNzr1j5OPh4vV_H3c2Z5yqVljU/edit?usp=sharing

##  Section 6: Risk Assessment  
    - https://docs.google.com/spreadsheets/d/13BJcJr0humsAPecGed6ze-h4i2a-5MenrYtKxfElhqc/edit?usp=sharing

##  Section 7: Support Requests
    - Right now, I'm not really needing any help other than if I'm implementing my solutions correctly. Luckily, I've been able to ask my capstone related questions while in class. But if that changes, you bet you that I'll be logging into office hours. If there's one thing I've learned throughout pathways is that it never hurts to be proactive and ask for help when you need it.
