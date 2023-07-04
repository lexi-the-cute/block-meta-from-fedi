# What's This About

Meta is planning on joining the Fediverse via a project called Project 92, or P92 for short. Many people including myself know how Meta is bad when it comes to respecting human rights. I'm not even just talking about Cambridge Analytica, but am talking about the [genocide which Meta helped perpetuate such as in Myanmar](https://www.amnesty.org/en/latest/news/2022/09/myanmar-facebooks-systems-promoted-violence-against-rohingya-meta-owes-reparations-new-report/). [Meta also has a history of mistreating queer people](https://www.aclu.org/news/lgbtq-rights/facebooks-discrimination-against-the-lgbt-community) and that's not even including the ["real" name policy](https://www.eff.org/deeplinks/2014/09/facebooks-real-name-policy-can-cause-real-world-harm-lgbtq-community). Of course, for me, I say that the name the person tells you is there name, is there real name. Not the name they were born with or their legal name, but the name that the person identifies with.

To help explain why the reaction is so strong against Meta, it helps to know that the Fediverse is very, very queer. The Fediverse is made of people, including LGBT people who had to flee from other platforms due to the abuse they've received from the platforms they used to be on. This includes the large influx of people which came from Twitter when Musk took over and started implementing transphobic policies and hiding trans people's tweets while allowing transphobic tweets and slurs to proliferate. Meta only wants to connect to the Fediverse because they see it as a means to make a profit, and they'll do that no matter how much it harms people or tears about the community.

You can read more about Meta and the Fediverse at the article, [Should the Fediverse welcome its new surveillance-capitalism overlords?](https://privacy.thenexus.today/should-the-fediverse-welcome-surveillance-capitalism)

You can also check out [the pact against Meta](https://fedipact.online) as well as [the explanation for the pact](https://fedipact.online/why).

# What's This Repo

This repo is a means to forcibly remove Meta from the Fediverse, by any means necessary. I've started this to collect a list of ip addresses which are owned by Meta and then to block Meta in ways that'll make life much more difficult for them. This includes silently dropping packets without notifying Meta, so their computers have to time out for each server which uses this method, as well as sending fake ActivityPub data to Meta and also throttling the connection, so as to slow their computers down and to make it harder for them to differentiate between which data is real, and which data is fake. It'll make their data much less valuable to anyone wanting to buy it.

# Will They Actually Harm Me?

I'll let you read this info provided by Meta themselves.

<br>

## Description of Threads App on the Apple Store

![Description of Threads App On the Apple Store](.readme/threads-apple-store-description.png)

If you can't read the image, I copied the text below.

```
Say more with Threads — Instagram’s text-based conversation app

Threads is where communities come together to discuss everything from the topics you care about today to what’ll be trending tomorrow. Whatever it is you’re interested in, you can follow and connect directly with your favorite creators and others who love the same things — or build a loyal following of your own to share your ideas, opinions and creativity with the world.

Meta Terms: https://www.facebook.com/terms.php
Threads Supplemental Terms: https://help.instagram.com/769983657850450
Meta Privacy Policy: https://privacycenter.instagram.com/policy
Threads Supplemental Privacy Policy: https://help.instagram.com/515230437301944
Instagram Community Guidelines: https://help.instagram.com/477434105621119
```

<br>

## App Privacy Description on the Apple Store

![App Privacy Description on the Apple Store](.readme/threads-apple-store-app-privacy.png)

As per usual, the text version is below.

```
App Privacy

The developer, Instagram, Inc., indicated that the app’s privacy practices may include handling of data as described below. For more information, see the developer’s privacy policy.
Data Linked to You

The following data may be collected and linked to your identity:

* Health & Fitness
* Purchases
* Financial Info
* Location
* Contact Info
* Contacts
* User Content
* Search History
* Browsing History
* Identifiers
* Usage Data
* Sensitive Info
* Diagnostics
* Other Data
```

<br>

## Description of Threads App on the Google Play Store

![Description of Threads App On the Google Play Store](.readme/threads-google-store-description.png)

The text version of the screenshot is below.

```
Threads, an Instagram app

About this app

Threads is where communities come together to discuss everything from the topics you care about today to what’ll be trending tomorrow. Whatever it is you’re interested in, you can follow and connect directly with your favorite creators and others who love the same things — or build a loyal following of your own to share your ideas, opinions and creativity with the world.

Meta Terms: https://www.facebook.com/terms.php
Threads Supplemental Terms: https://help.instagram.com/769983657850450
Meta Privacy Policy: https://privacycenter.instagram.com/policy
Threads Supplemental Privacy Policy: https://help.instagram.com/515230437301944
Instagram Community Guidelines: https://help.instagram.com/477434105621119
````

<br>

## App Privacy Description on the Google Play Store

![App Privacy Description on the Google Play Store](.readme/threads-google-store-app-privacy.png)

As per usual, the text version is below.

```
Threads, an Instagram app

# Data shared
## Data that may be shared with other companies or organizations

* Personal info
## Name, Email address, User IDs, and Phone number

* Device or other IDs
## Device or other IDs

# Data collected
## Data this app may collect

* Location
## Approximate location and Precise location

* Personal info
## Name, Email address, User IDs, Address, Phone number, Political or religious beliefs, Sexual orientation, and Other info

* Financial info
## User payment info, Purchase history, Credit score, and Other financial info

* Health and fitness
## Health info and Fitness info

* Messages
## Emails, SMS or MMS, and Other in-app messages

* Photos and videos
## Photos and Videos

* Audio
## Voice or sound recordings, Music files, and Other audio files

* Files and docs
## Files and docs

* Calendar
## Calendar events

* Contacts
## Contacts

* App activity
## App interactions, In-app search history, Installed apps, Other user-generated content, and Other actions

* Web browsing
## Web browsing history

* App info and performance
## Crash logs, Diagnostics, and Other app performance data

* Device or other IDs
## Device or other IDs

# Security practices

* Data is encrypted in transit
## Your data is transferred over a secure connection

* You can request that data be deleted
## The developer provides a way for you to request that your data be deleted

For more information about collected and shared data, see the developer's privacy policy (http://instagram.com/legal/privacy)
```

At the time of writing, the website just contains a countdown and the [privacy policy](http://instagram.com/legal/privacy) links to Instagram.

* [Apple App Store Listing](https://apps.apple.com/us/app/threads-an-instagram-app/id6446901002)
* [Google Play Store Listing](https://play.google.com/store/apps/details?id=com.instagram.barcelona&gl=it)
* [Website](https://www.threads.net/)

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

I intentionally set everything in this repo as Public Domain (or [CC0 1.0 Universal](License.md) where Public Domain does not exist). This way anyone can work on improving this anti-Meta measure without restriction./