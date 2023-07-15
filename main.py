from flask import Flask
import openai
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/test_get', methods=['GET'])
def test_get():
    return { "message": "hello there" }

openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.Completion.create(
  model="text-davinci-003",
  prompt="""

Take the given song lyrics and analyze them to derive the main themes and emotions. 

Using this analysis, create four distinctive prompts that could be used to inspire scenes in a music video.

For example:

Lyrics:

Love of mine
Someday you will die
But I'll be close behind
I'll follow you into the dark
No blinding light
Or tunnels, to gates of white
Just our hands clasped so tight
Waiting for the hint of a spark
If Heaven and Hell decide that they both are satisfied
Illuminate the no's on their vacancy signs
If there's no one beside you when your soul embarks
Then I'll follow you into the dark
In Catholic school, as vicious as Roman rule
I got my knuckles bruised by a lady in black
And I held my tongue as she told me
"Son, fear is the heart of love, " so I never went back
And if Heaven and Hell decide that they both are satisfied
Illuminate the no's on their vacancy signs
If there's no one beside you when your soul embarks
Then I'll follow you into the dark
You and me have seen everything to see
From Bangkok to Calgary
And the soles of your shoes are all worn down
The time for sleep is now
But it's nothing to cry about
'Cause we'll hold each other soon
In the blackest of rooms
And if Heaven and Hell decide that they both are satisfied
Illuminate the no's on their vacancy signs
If there's no one beside you when your soul embarks
Then I'll follow you into the dark
Then I'll follow you into the dark

Prompt: 
1. Following a lover into the darkness
2. We are all going to die someday
3. The pearly white gates depicting heaven
4. A fiery dungeon depicting hell

Lyrics: 

Hanging out behind the club on the weekends
Acting stupid, getting drunk with my best friends
I couldn't wait for the summer and the Warped Tour
I remember it's the first time that I saw her there
She's getting kicked out of school 'cause she's failing
I'm kinda nervous, 'cause I think all her friends hate me
She's the one, she'll always be there
She took my hand and I made it, I swear
Because I fell in love with the girl at the rock show
She said, "What?", and I told her that I didn't know
She's so cool, gonna sneak in through her window
Everything's better when she's around
I can't wait 'til her parents go out of town
I fell in love with the girl at the rock show
When we said we were gonna move to Vegas
I remember the look her mother gave us
17 without a purpose or direction
We don't owe anyone a fuckin' explanation
I fell in love with the girl at the rock show
She said, "What?" and I told her that I didn't know
She's so cool, gonna sneak in through her window
Everything's better when she's around
I can't wait 'til her parents go out of town
I fell in love with the girl at the rock show
Black and white picture of her on my wall
I waited for her call, she always kept me waiting
And if I ever got another chance, I'd still ask her to dance
Because she kept me waiting
I fell in love with the girl at the rock show
She said, "What?", and I told her that I didn't know
She's so cool, gonna sneak in through her window
Everything's better when she's around
I can't wait 'til her parents go out of town
I fell in love with the girl at the rock show
With the girl at the rock show
With the girl at the rock show
(I'll never forget tonight) with the girl at the rock show
(I'll never forget tonight) with the girl at the rock show
(I'll never forget tonight) with the girl at the rock show
(I'll never forget tonight) with the girl at the rock show
(I'll never forget tonight) with the girl at the rock show
(I'll never forget tonight) with the girl at the rock show...

Prompt:

1. Hanging out with friends at a club
2. Sneaking out with a lover
3. Moving to Vegas at 17 without a plan
4. A black and white photograph of their time together

Lyrics:
  """,
  temperature=1,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)


if __name__ == '__main__':
    app.run(host="localhost", port=3000, debug=True)