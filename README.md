# Natural Language Processing
Using NLP to set reminders in Google Calendar

## PROBLEM STATEMENT:-
Given a query related reminders, Detect the custom message/phrase that user wants to set reminder for(If present).
E.g: Please remind me to go to gym
Remind Phrase: "Go to gym"
## Approach
This was fairly siimple and could be done by simple string manipulation.I decided to take it a step higher.
I used a Speech-to-Text API which enabled me to take user input in from of speech.This speech was then converted to text which was passed to the NLP model.I used spaCy library to prosess the query.The words from this query were first tokenized and then were segregated in their respective POS (Part Of Speech) lists. I used the combination of words from verb and noun list to detect/create the task which user wants to be reminded of. Date and time were extracted with the help of 'dateparser' library. The date was stored in dd-mm-yyyy format and the time was stored in 24 hours format.
This task,time and date are then passed into Google Calendar API. 
The event gets created in the Google Calendar and the user gets a notification about the same.
