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

## intent:request_triage
- Do I have corona?
- How do I know if I have corona?
- Where can I get tested?

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

## regex:number
- [0-9]+

## intent:inform
- [0](number)
- [1](number)
- [2](number)
- [3](number)
- [4](number)
- [5](number)
- [6](number)
- [7](number)
- [8](number)
- [9](number)
- [10](number)
- for [myself](person:self)
- [i](person:self) am
- [me](person:self)
- yes [I](person:self) am
- im taking it for [me](person:self)
- for my [child](person:other)
- [someone else](person:other)
- for my [mother](person:other)
- I'm taking it for a [relative](person:other)
- it's for my [neighbor](person:other)
- I have a [cough](symptom:cough)
- I've been [coughing](symptom:cough)
- I [can't breathe](symptom:sob)
- I feel like my [lungs are full of fluid](symptom:sob)
- She's [burning up](symptom:fever)
- I have a [fever](symptom:fever)
- He has [diarrhea](symptom:diarrhea)
- I have [dioreha](symptom:diarrhea)
- This morning I had [dierea](symptom:diarrhea)
- Last night I had [diorhea](symptom:diarrhea)
- Yes, last night I had [diorhea](symptom:diarrhea)
- I [can't taste](symptom:losot) anything.
- Yeah, I [can't taste](symptom:losot) anything.
- I [can't smell](symptom:losot).
- I can't stop [coughing](symptom:cough).
- yes I'm [coughing](symptom:cough).

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

## intent:worried
- I am scared of how I will die.
- I am afraid of the upcoming economic crisis in the USA.It will affect all of us.
- I think small things make me worried
- I had to go to the doctor recently to get something checked, always makes me worried going there.
- I have a court date next week and I don't know what's going to happen.  I really want custody of my kids.
- I am worried I won't wake up to my alarm
- I am old and in good health, but death is around the corner.
- My friend's eyes keep hurting at night. She's been to the doctor, but they can't find anything wrong with her
- My brother is in the hospital and is very sick. I am very scared

## intent:stressed
- I am stressed by my blood test results that I will have tomorrow.
- Yesterday I went to the doctor and had to get a shot.
- I had to have some extra tests ran a few weeks back due to an unclear mammogram.
- I can't work.
- I recently had an existential crisis. It was awful
- I have a presentation to prepare for this week and I am finding it really hard to meet the deadline. I am so stressed
- I am really nervous.  I have to go tomorrow to get my tooth pulled and I am scared to death.  I hate the dentist!
- I am worried about my surgery next week. I have never had to get surgery before!
- I am so nervous.  I have to take a really important exam next week.
- I was scared that I was gonna die
- I am so stress. Tomorrow, I will have my final exams.
- I am stressed. My wife is expecting a baby. I am happy but at the same time I feel littlle stresse by the responsibilities.
- I always feel nervous in a crowd.
- I just watched the testimony before Congress today. It was quite a show. 
- I am about to enter the workforce again soon. Hopefully
- I often feel a lot of anxiety about making enough money and saving up enough money in case anything happens. 
- I always get nervous when I drive. The possibility of getting into a car accident is nerve wrecking.
- I am hoping to become an English teacher but I am waiting on test results to come back.
- I hate storms so much. We are supposed to be getting bad storms tonight.
- I have a math test tomorrow and it is the biggest one of the semester.
- I need to find a new job soon
- I lost my job
- I think our job might be laying us off.
- I recently lost my job, and am having trouble finding another one. 
- I thought my girlfriend was pregnant recently. 
- I thought I would be homeless once and I was having a major panic attack. I was minutes from being homeless.
- I can't stop watching the news
- my kids are stressing me out
- I cant do all this

## intent:need_sleep
- I have a difficult falling asleep before a job interview
- I am so tired
- I can barely keep my eyes open
- I can't sleep with everything going on
- I am having trouble getting to sleep
- I have a difficult falling asleep before a job interview
- I couldn't sleep last night at all, I kept hearing some weird bumping sounds that made me think someone was walking up and down my stairs but I live alone.
- I was always afraid to go to sleep as a kid.
- I hardly got any sleep last night
- I couldn't go back to sleep
- I am exhausted
- I do not like the dark

## intent:social_isolation
- I'm lonely
- I am alone
- I don't have friends
- My family hasn't called
- No one has called me
- You're all I have
- You're the only one that I can talk to
- My friends are all dead
- I have no family
- I haven't seen or talked to anyone in weeks

## intent:crisis
- I need help
- I don't have anything to eat


## intent:financial_stress
- I'm going to lose my house
- I got an eviction notice
- I don't know where I am going to live
- i am worried about money
- i am scared I may lose my job
- are we going to enter a recession?

## intent:suicidal
- I'm going to kill myself
- I want to die
- I see no point in living anymore

## intent:emergency
- I'm having a heart attack
- I can't breathe
- He is having trouble breathing
- He is coughing blood

## intent:frustrated
- I can't do this anymore
- I'm frustrated
- tired of being at home
- sick of working from home
- My kids won't stop bothering me
- I can't wait for the kids to go back to school

## intent:sad
- working from home is not fun
- i'm depressed
- this is depressing
- i'm sad


## intent: