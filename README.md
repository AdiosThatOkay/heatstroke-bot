# heatstroke-linebot

LINE Messaging Chat Bot that will notify WBGT.  
WBGT data **(Japan only!)** is provided by [Japan Ministry of Environment.](http://www.wbgt.env.go.jp/)

Let's prevent Heat Stroke!!

## Demo

## Requirement

* LINE Developers account
* [Docker](https://docs.docker.com/install/)
* Certificate file and Key file

## Features

- Giving you WBGT information of today by Push Message everyday 7:00(JST).
- You talk as follows,
  - 今, now, 今日, today -> Giving you WBGT information of today.
  - 明日, あす, tomorrow -> Giving you tomorrow WBGT forecast.
  - 明後日, あさって, day after tomorrow -> Giving you ... (as you think)
- You send location, Switch to the nearest Observatory from sent location.
- WBGT is higher than or equal 31 degrees, notify you caution by Push Message.

## Install

### 1- Create your LINE Channel

- Login or Sign up on [LINE Developers](https://developers.line.biz/ja/).
- Create LINE Channel using Messaging API.
- Remember Channel Secret and Access Token(Long Term).
  - If you don't have Access Token, click the reissue button.

### 2- Deploy the BOT

- clone this repository.
- Set `LINE_CHANNEL_ACCESS_TOKEN` on the `Dockerfile` to your Access Token(Long Term).
  - You use `docker-compose.yml`, see the below.
- **You must build Reverse Proxy server.** Recommend one (and I use) is [jwilder/nginx-proxy](https://github.com/jwilder/nginx-proxy).  
`docker-compose.yml` using [jwilder/nginx-proxy](https://github.com/jwilder/nginx-proxy) looks like this:
```yaml
version: '3'
services:
  proxy:
    image: jwilder/nginx-proxy
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - path/to/cert/directory:/etc/nginx/certs
      - /var/run/docker.sock:/tmp/docker.sock:ro
services:
  heatstroke-linebot:
    build: .
    environment:
      VIRTUAL_HOST: YOUR-APP-NAME
      LINE_CHANNEL_ACCESS_TOKEN: YOUR-CHANNEL-ACCESS-TOKEN
      LINE_CHANNEL_SECRET: YOUR-CHANNEL-SECRET
    expose:
      - "9090"
    volumes:
      - data:/app/hsbot/database

volumes:
  data:
    driver: "local"
```
and exec this
```sh
docker-compose build
docker-compose up -d
```

### 3- Setting your LINE Channel

- Set the using Webhook enable.
- Edit Webhook URL `https://{YOUR-APP-FQDN}/callback`
  - Connection check fails but works properly.

### 4- Follow your Bot

- Read the QR Code on your smartphone.

## Contribution

1. Fork [this repository](https://github.com/AdiosThatOkay/heatstroke-linebot)
2. Create your feature branch (git checkout -b my-new-feature)
3. Commit your changes (git commit -am 'Add some feature')
4. Push to the branch (git push origin my-new-feature)
5. Create new Pull Request

## Licence

[MIT](https://github.com/tcnksm/tool/blob/master/LICENCE)

## Author

[AdiosThatOkay](https://github.com/AdiosThatOkay)
