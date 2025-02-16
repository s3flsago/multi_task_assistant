# language_practice_assistant
The language practice assistant is a telegram chatbot that can help the student to learn foreign languages.

# Development:
`pip install -r requirements.txt`
`. startup.sh`

# Testing:


# How to to run the assistant:
- Build docker image: `docker build -t language_practice_assistant:0.1 .` 
- Run the container: `docker run  language_practice_assistant:0.1 /bin/bash`

# How to study:
- Launch telegram on your phone or desktop computer
- create a bot with the Telegram "BotFather"
- Say hello to the assistant to start the session. He will provide you with all necessary information. Happy learning :)

# Example Usage

```plaintext
User: Hi!  

Bot: Hello! How many verbs would you like to quiz today, and in which language?  

User: Three verbs in Spanish, please.  

Bot: Great choice! Let's start with the first verb.  
     What is the form of "ser" for "él/ella" in the "futuro indicativo"?  

User: Seré  

Bot: That's close, but not quite right!  

     The correct form of "ser" for "él/ella" in the "futuro indicativo" is **"será."**  

     Here's a quick reference for "ser" in the "futuro indicativo":
     - yo **seré**
     - tú **serás**
     - él/ella **será**
     - nosotros **seremos**
     - vosotros **seréis**
     - ellos/ellas **serán**

     Now, let's move on to the next verb!  
     What is the form of "caber" for "nosotros" in the "subjuntivo presente"?  
