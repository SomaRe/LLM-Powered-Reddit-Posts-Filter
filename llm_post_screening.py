from openai import OpenAI
import json
import os
import dotenv

dotenv.load_dotenv()

# Configure OpenAI API key
client = OpenAI(
    api_key= os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL"),
)


def check_post_with_llm(prompt):
    try:
        response = client.chat.completions.create(
            model=os.getenv("LLM_MODEL"),
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            response_format={ "type": "json_object" }
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        return None


    data = [
        {'title' : "[USA-NJ][H] Dell Latitude 7430 & Dell XPS 15 7590 Both w/ Dell Warranty [W] PayPal",
         'description' : """Latitude 7430

• i5-1245U

• 16GB RAM (Soldered)

• 512GB SSD

• Fingerprint Sensor

• Face Unlock IR Camera

• Basic Dell Warranty until Feb. 2026 (ST: HBVLCK3)

• New 60W USB C charger

• Asking $350 Shipped OBO

XPS 15 7590

• i7-9750H

• 16GB RAM (2x8GB)

• 1TB NVME SSD

• NVIDIA GTX 1650 4GB

• Fingerprint Sensor

• Basic Dell Warranty until November 2024 (ST: BDQBP73)

• No Charger included. Requires 130W 4.5mm Dell power adapter which I do not have on hand. Will charge over USB C/Thunderbolt as well.

• Asking $400 Shipped OBO"""
         },
         {
            'title' : "[GIVEAWAY] BNIB ASUS TUF Gaming GTX 1650 Super GPU",
            'description' : """Welcome to Giveaway Weekend #17! It's been a long while since I've done one of these and it's time to do it once again. Today's item was chosen out from Microcenter (not sponsored) and I thought it would be a good choice given the current market. Hopefully one of you can enjoy an ASUS GTX 1650 Super and make good use of it. I know it's nowhere near 30 series performance, but it can still do good work for 1080p gaming. I did purchase a 2 year warrantee with it, but I'm not sure if it's transferable tbh.

Timestamp: https://imgur.com/a/Eyihvo0

This giveaway will run until 5pm EST on March 22nd (~48 hours) and is to follow the guidelines established in this post

To enter, all you need to do is comment below and follow the giveaway rules!

Below are some rules on the giveaway itself:

Only enter this giveaway if you will have a use for this item, otherwise, a new post will have to be made if you change your mind.

You can only enter this giveaway if your account meets the minimum requirements to make a post on the subreddit. (100 COMMENT Karma or an account age of at least 50 days). Asking for karma will get you permanently banned from the subreddit.

You must be an active participant in this or other subreddits. Accounts that only have comments in giveaways will have their entries removed. If chosen, your profile will be reviewed to make sure you meet this requirement.

You must not use a blind reshipper to get around country limitations. You may put in your entry that you will use a reshipper, but if the giveaway operator chooses your entry, they may choose to draw again if they wish."""
         }
    ]

    for post in data:
        title = post['title']
        description = post['description']
        test_prompt = f"""Analyze the following Reddit post and determine if it contains a laptop for sale.
        Return a JSON object with a single key "contains_laptop" and a boolean value.

        Title: {title}
        Description: {description}"""

        result =  json.loads(check_post_with_llm(test_prompt))
        print(f"LLM Response: {result}")