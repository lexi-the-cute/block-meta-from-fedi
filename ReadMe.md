# What's This About

Meta is planning on joining the Fediverse via a project called Project 92, or P92 for short. Many people including myself know how Meta is bad when it comes to respecting human rights. I'm not even just talking about Cambridge Analytica, but am talking about the [genocide which Meta helped perpetuate such as in Myanmar](https://www.amnesty.org/en/latest/news/2022/09/myanmar-facebooks-systems-promoted-violence-against-rohingya-meta-owes-reparations-new-report/). [Meta also has a history of mistreating queer people](https://www.aclu.org/news/lgbtq-rights/facebooks-discrimination-against-the-lgbt-community) and that's not even including the ["real" name policy](https://www.eff.org/deeplinks/2014/09/facebooks-real-name-policy-can-cause-real-world-harm-lgbtq-community). Of course, for me, I say that the name the person tells you is there name, is there real name. Not the name they were born with or their legal name, but the name that the person identifies with.

To help explain why the reaction is so strong against Meta, it helps to know that the Fediverse is very, very queer. The Fediverse is made of people, including LGBT people who had to flee from other platforms due to the abuse they've received from the platforms they used to be on. This includes the large influx of people which came from Twitter when Musk took over and started implementing transphobic policies and hiding trans people's tweets while allowing transphobic tweets and slurs to proliferate. Meta only wants to connect to the Fediverse because they see it as a means to make a profit, and they'll do that no matter how much it harms people or tears about the community.

You can read more about Meta and the Fediverse at the article, [Should the Fediverse welcome its new surveillance-capitalism overlords?](https://privacy.thenexus.today/should-the-fediverse-welcome-surveillance-capitalism)

You can also check out [the pact against Meta](https://fedipact.online).

# What's This Repo

This repo is a means to forcibly remove Meta from the Fediverse, by any means necessary. I've started this to collect a list of ip addresses which are owned by Meta and then to block Meta in ways that'll make life much more difficult for them. This includes silently dropping packets without notifying Meta, so their computers have to time out for each server which uses this method, as well as sending fake ActivityPub data to Meta and also throttling the connection, so as to slow their computers down and to make it harder for them to differentiate between which data is real, and which data is fake. It'll make their data much less valuable to anyone wanting to buy it.

# Does This Work?

As of the latest test at the time of writing this paragraph, I have confirmed that this script does block Meta's implementation of an ActivityPub server, threads.net.

![Terminal Output Testing Threads.net IP Block](/.readme/threads-net_block_test.png)

For those who can't read the image, I pasted a copy of the output below.

```bash
# dig threads.net +short
31.13.65.52

# dig www.threads.net +short
threads.net.
31.13.65.52

# dig -x 31.13.65.52 +short    
instagram-p3-shv-01-atl3.fbcdn.net.

# python3 main.py -f plain | grep -i "31.13.65"
31.13.65.0/24
```

# What Else Can We Do

You can always sign the [the pact against Meta](https://fedipact.online) as well as update people with new Meta instances via the #FediBlock hashtag. You can also contribute means of obtaining lists of Meta's servers by ip, and domain. This list can include both scrapers, and ActivityPub powered instances.

If you're a server owner, you can also update your .env.production file if you'd like to make it harder for others to read posts without authentication, however, this may make things less convenient for your denizens. I'd advise [reading about these options](https://hub.sunny.garden/2023/06/28/what-does-authorized_fetch-actually-do/) and consulting with your denizens before you enable them.

```ini
AUTHORIZED_FETCH=true
DISALLOW_UNAUTHENTICATED_API_ACCESS=true
```

I intentionally set everything in this repo as Public Domain (or [Unlicense](License.md) where Public Domain does not exist). This way anyone can work on improving this anti-Meta measure without restriction.