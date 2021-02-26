# DeepDreams
Downloading all of **my personally created** *Deep Dreams* from [deepdreamgenerator.com](https://deepdreamgenerator.com)

## Note
The script to download dreams off of Deep Dream Generator requires the python3 requests library, as well as Beutiful Soup.
It also uses urllib and math but those *should* be installed by default I believe.

Install them by running the following commands in a command prompt / unix shell:

``pip3 install requests``

``pip3 install beautifulsoup4``

## Usage
Use the get_deepdreams.py script.

Change the following to match your login:

username - this is found in the URL of your account page

payload.email - this should be your email that you use to login to Deep Dream Generator

payload.password - this should be your password for Deep Dream Generator

Provide the script with either "1", "2" or "3" for an input.

1: The original way I downloaded dreams, this does the "latest" page. Dreams are downloaded with their DDG file names. Only public dreams will be downloaded.

2: The second way I started downloading dreams. This does the "best" page. Dreams are downloaded with a filename like "dream_num###.jpg" where the number is the order it was found on the best page. So you end up with "dream_num1.jpg" being your top liked dream. And a dream like "dream_num999.jpg" might be one of your least liked dreams.

3: The final way I decided to download my dreams. This downloads ALL dreams found on your "account" page or under the "My Files" tab on your DDG profile. Dreams are downloaded with their original DDG file names. The main difference for this options is you get ALL dreams, even the ones you didn't publicly post. This is a good way to backup all your dream creations for future use incase DDG ever shuts down.

Read the **¡¡ WARNING !!** for important info but the TL&DR is **DO NOT** use other people's accounts with this script!

## ¡¡ WARNING !!
Deep Dream Generator states on the [Deep Dream Generator FAQ/Info Page](https://deepdreamgenerator.com/info) the following:

> You can use the "+" button to use other user's style but it is not allowed to download the style image itself. It is not allowed to download or use the base image of other user's Dream. Also it is not allowed to use the result, Dream image from other users.

Thus, you should not use this code to download other people's dreams. I only recommend downloading your personal dreams, which is what I made this tool to do since Deep DReam Generator currently doesn't have an option to download your dreams. Violating the Deep Dream Generator rules will get your account banned, so don't do that. And it's not nice to slam other people's websites. >:(

## License
This code is licensed under the MIT License, thus I am not responsible for whatever fires you cause by using this code. YMMV, test it with some break points and stuff before trying to download a ton of dreams. And who knows if this code still works when you read this - the Deep Dream Generator website might have changed their dream page HTML, and broken this code.