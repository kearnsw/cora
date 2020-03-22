## intent:greet
- hey
- hello
- hi
- good morning
- good evening
- hey there
- howdy

## intent:update_symptoms
- I'd like to update my symptoms
- change my symptoms
- Symptoms
- update my symptoms

## intent:find_testing
- Where can i get tested
- where are the testing sites
- Where do they do tests
- Are there any tests near me
- how do i get tested
- i need testing
- tests

## intent:mental_health
- I'm lonely
- I am alone
- I feel stressed
- I can't stop watching the news
- I'm so anxious
- I can't do this anymore
- I'm frustrated
- tired of being at home
- sick of working from home
- my kids are stressing me out
- working from home is not fun
- i am worried about money
- i am scared I may lose my job
- are we going to enter a recession?
- i can't take it anymore
- i'm depressed
- this is depressing
- I cant do all this

## intent:goodbye
- bye
- goodbye

## intent:affirm
- yes
- indeed
- of course
- that sounds good
- correct
- definitely
- sure

## intent:deny
- no
- never
- I don't think so
- don't like that
- no way
- not really

## regex:rating
- [0-9][0]?

## intent:inform
- [0](rating)
- [1](rating)
- [2](rating)
- [3](rating)
- [4](rating)
- [5](rating)
- [6](rating)
- [7](rating)
- [8](rating)
- [9](rating)
- [10](rating)

## intent:describe_mood
- I feel [tired](state)
- I'm [coughing alot](state)
- I am so [bored](state)
- I [want to be with my friends](state)

## intent:ask
- What's that?
- What's contact?
- how do i know if i've come in contact?

## intent:version
- version
- show version
- what version
- what's your version
- show build date
- what is your build date
- what's your build
- show model version
