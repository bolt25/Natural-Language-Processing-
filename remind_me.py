import spacy
import datetime
import dateparser
import google_cal as cal                 #importing google calendar api 
import speech                            # importing speech to text api

word_list=[]

nlp=spacy.load('en_core_web_sm')         #loading en_core_web_sm model from spaCy

query = str(speech.press_record())       #converting speech to text using speech_to_text API 

print(query)      

for word in query.split(' '):
  wk = word
  word = word.replace("th","")
  word = word.replace("rd","")
  word = word.replace("st","")
  word = word.replace("nd","")
  try:
    temp = int(word)
    if len(word==1):
      word = "0"+word 			  #to convert 1,2,3,.... to 01,02,03.....
      query = query.replace(wk,word)
  except:
    pass

doc=nlp(query)   			                    #tokenizing the query

adjs=[]     				                      '''initiating an adjective list
                                             (bcoz numbers in date like 5 in 5th December is recognized as an adjective instead of date)'''
for token in doc:                         

  if token.pos_=="ADJ":                   
    adjs.append(token.text)               #creates a list of numbers from which the date starts

for token in doc:
  word_list.append(token.text)            #creates a list of tokenized words


'''
Checking if Remind phrase is present or not
'''

if "Reminder" in word_list or "Remind" in word_list or "remind" in word_list or "reminder" in word_list:

  '''Verb list'''
  def verb(x):
    verb_list=[]
    for token in x:
      if token.pos_=='VERB':
        verb_list.append(token.text)   
    return verb_list

  '''Noun list'''
  def noun(x):
    noun_list=[]
    for token in x:
      if token.pos_=='NOUN':
        noun_list.append(token.text)
    return noun_list

  '''Date list'''
  def date(x):
    date_list=[]
    for token in x.ents:
      if token.label_=='DATE':
        date_list.append(token.text)
    return date_list

  '''Time list'''
  def time(x):
    time_list=[]
    for token in x.ents:
      if token.label_=='TIME':
        time_list.append(token.text)
    return time_list

  Noun=noun(doc)
  Verb=verb(doc)

  for i in Noun:
    if 'p.m.' in Noun:
      Noun.remove('p.m.')
    if 'a.m.' in Noun:
      Noun.remove('a.m.')                # a.m. ,p.m. is labelled as nouns, so we drop those from the noun list

    time_set=dateparser.parse(time(doc)[0],settings={'TIMEZONE': 'UTC-5:30'})     #getting the time from the query


    hour,mins,secs=time_set.hour,time_set.minute,time_set.second      #getting hours, minutes and seconds from time_set

    if not date(doc):                                                 #setting today's date as default if user doesn't specify any particular date
      default_date=datetime.datetime.now()
      day,month,year=default_date.day,default_date.month,default_date.year
    else:                                                             #getting today's date if user provides it in the query
      date_set=dateparser.parse(date(doc)[0],settings={'PREFER_DATES_FROM': 'future'})
      day,month,year=date_set.day,date_set.month,date_set.year

    
    '''
    Displaying task
    '''

    if not Noun:
      task=(Verb[1])
    else:
      task=(Verb[1]+' '+Noun[0])

    print(task ,'at',hour,':',mins,':',secs,'on',day,'-',month,'-',year)

    start = str(str(year)+"-"+str(month)+"-"+str(day)+  " T "  +str(hour)+":"+str(mins)+":"+str(secs)+"+05:30")
    end = str(str(year)+"-"+str(month)+"-"+str(day)+  " T "   +str(hour)+":"+str((mins+5))+":"+str(secs)+"+05:30")
    service = cal.auth()                 #calling google calender api
    cal.event(service,task,start,end)    #creating the event
    cal.upcomingEvent(service)           #printing the upcoming events
      

 
else:                                    #if the phrase 'remind' or 'Remind' is not present in the query the program won't do anything.
  print('Okay,I won\'t Remind you anything')
