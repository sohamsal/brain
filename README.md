# brain
here's an example: https://twitter.com/sohamsal/status/1806161229855044080

until i figure out how to make this run from a server, here's a guide on how to run this locally:

1. download free for personal/commerical-use subway surfers/minecraft parkour footage from youtube. [cobalt.tools](https://cobalt.tools) is a great way to download videos without ads

2. start a virtual environment

3. install dependencies with `pip install -r requirements.txt`

4. replace essay.txt with any text-based content you want to make a video on

5. place downloaded footage in same directory as your project, and rename it to `footage.mp4`

6. put in your openai and groq api keys in exp.py (lines 14-15)

    `client = OpenAI(api_key="YOUR OPENAI API KEY HERE")`
    `groqC = Groq(api_key="YOUR GROQ API KEY HERE")`

    or you could use the same openai key and just change the model in gen_tts() function (line 22)

    from `model="llama3-70b-8192"` to `model="gpt-3.5-turbo"` or any openai model for that matter

7. download imagemagick 
    - wsl/linux: https://gist.github.com/cuuupid/963db645047597723956af13ab87b73a
    - mac: `brew update && brew install imagemagick` 
    - windows: https://imagemagick.org/script/download.php#windows

8. run `python exp.py` from terminal
