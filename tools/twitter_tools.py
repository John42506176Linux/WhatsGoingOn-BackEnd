import re
from models.event_model import Event
from models.tweet_model import TweetEvent

def process_tweet(model,content, publish_date, parser, prompt, gpt_list):
    try:
        input = get_twitter_contents(content.extract)
        _input = prompt.format_prompt(tweet=input['tweet'],publish_date=publish_date)
        output = model(_input.to_string())
        output = parser.parse(output)
        output = TweetEvent.fromEvent(event = output, retweet_count = input['retweets'], favorite_count = input['favorites'], reply_count = input['replies']).dict()
        output['url'] = content.url
        output['source'] = 'Twitter'
        gpt_list.append(output)
    except Exception as e:
        print(e)
        pass

def get_twitter_contents(extract: str):
    tweet = extract.split('| created_at')[0].replace("<div>", "", 1)
    retweet_count = int(re.search(r'retweet_count: (\d+)', extract).group(1))
    reply_count = int(re.search(r'reply_count: (\d+)', extract).group(1))
    favorite_count = int(re.search(r'favorite_count: (\d+)', extract).group(1))
    return {'tweet': tweet, 'retweets': retweet_count, 'replies': reply_count, 'favorites': favorite_count}
