import os
from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse
from story import write_story, append_to_story

app = Flask(__name__)
# if for some reason, your conversation with the chef gets weird, change the secret key 
app.config['SECRET_KEY'] = 'fu3rdtimecharm!'

@app.route('/bot', methods=['POST'])
def ghost_writer():
    incoming_msg = request.values['Body']
    session_story = session.get('session_story')
    story = write_story(session_story)

    file1 = open("spookystory.txt","a") 
    if (os.stat("spookystory.txt").st_size == 0): 
        print("Empty file") 
        file1.write("The following is a spooky story written for kids, just in time for Halloween. Everyone always talks about the old house at the end of the street, but I couldn’t believe what happened when I went inside.")
    if incoming_msg == "the end":
        msg = MessagingResponse()
        msg.message("To be continued...?")
        file1.close()
        return str(msg)
    session['session_story'] = append_to_story(story, session_story)
    file1.write(story)
    print("the session session_story = ", session_story)

    msg = MessagingResponse()
    msg.message(story)
    return str(msg)

if __name__ == '__main__':
    app.run(debug=True)