# discord-emoji-loader
Downloads discord emojis contained in an HAR file.

Possibly an edge case only relevant to me, but I wanted to download a bunch of Discord emojis for use on my own server. Problem is that discord bots can only access emojis on servers they were invited to, so this doesn't help with emojis of servers you don't own. Some client-side JS would have probably done the trick too, but this was a viable alternative.

Basically you open Discord's web client and start a network capture within Firefox while browsing the available emojis in the emoji finder. Then you save that as .har file, which contains all the URLs of the requested emojis.

This script extracts the URLs and downloads them. ezpz
