# **Daily FX Rates – Push Notification**

This task is part of my automation projects. Since I’m from Hungary, I’m certainly interested in foreign exchange rates regarding the Hungarian forint. Therefore, I want to be always informed about the latest exchange rates. I do not want to follow it minute by minute, using widgets on my phone or smartwatch, for example. It would be just fine to know about it once or twice a day, let’s say in the morning and in the afternoon. My idea was that I want to get a push notification about it, acknowledge the prices, then delete the notification. I was sure I could do that by downloading and subscribing to an application, but I wanted to solve this for myself. 

*This is one of the reasons I bought an old, refurbished Mac mini that I could use as an always-running home server. I can write tasks I want to be done automatically around my home and on my devices.*

The execution consists of three parts. First, I need to get the latest foreign exchange rates. Then, I have to send a formatted text about this data as a push notification to my phone. Finally, I want to repeat this task twice a day, every day— except for the weekends when the market is closed. Here is a chart about my idea of execution:

<img width="3490" height="2251" alt="ntfy-daily-fx-rates-flowchart" src="https://github.com/user-attachments/assets/ac567ca0-536d-4066-8e29-fe7ff3ea9555" />

Actually, during working on this project, I executed these three steps in a reversed order. I tested the automation method first, then selected the notifying system, and coded the data downloader last.

## **Automatising the process**

As I am a macOS user, I tried to use the native service manager, *launchd*. It has many advantages and would be perfect for more serious work. However, it proved to be too complicated for such small, repetitive tasks like this one. I stayed using a more universally known, one-liner job scheduler - *cron*. Here is the code snippet that I use for the morning schedule:

```bash
30 8 * * 1-5 /opt/anaconda3/bin/python3 /Users/.../Repositories/Daily-FX-Push-Notifications/ntfy-daily-fx-rates.py > /dev/null 2>&1
```

* At 08:30 AM, Monday to Friday (`1-5`)
* Run the Python script:
  `/Users/.../Repositories/Daily-FX-Push-Notifications/ntfy-daily-fx-rates.py`
  using Python from: `/opt/anaconda3/bin/python3`
* Redirect all output (stdout and stderr) to nowhere (`/dev/null`) - so it runs silently.

## **Sending push notifications**

There are several ways to send push notifications from your computer to your phone. The most customisable one is building your own app — which I deliberately wanted to avoid. Instead, I started to work on a web push service. Having little to no experience with how web development works, I soon realised that I should host a server that is rather complicated on my level. Therefore, I settled with a method that requires a third-party solution but is free to use — even if with limitations. I am using ntfy.sh, which is really easy to set up and work with.

In fact, anyone can subscribe to my updates:

1. Install the **ntfy** app
2. Subscribe to the topic: **daily-fx-rates**

## **Getting the required data**

Finally, getting the required data for an exchange rate. It could be a trivial task by Googling it, but since it is a repetitive task that needs to be executed every day, one should use some kind of service to download data. If you are subscribed to any financial data service, e.g. Bloomberg or LSEG, it is best to use them for this purpose. However, for this task, I wanted to have a completely free solution. Fortunately, many sites offer APIs that have a free-tier as well. I selected one of them (Open Exchange Rates), subscribed to them, and started downloading my data.

