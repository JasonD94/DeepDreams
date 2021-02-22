import os

# Now that we have a list of img URLs, download them to an img directory
# First, make sure an "img" directory exists
does_dir_exist = os.path.isdir("img")

if does_dir_exist is False:
    print("Making the img directory...")
    os.mkdir("img")
else:
    print("Img directory already exists :)")
