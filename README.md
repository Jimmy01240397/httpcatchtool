# httpcatchtool

A tool to listen http and dump.

## Init

```bash
bash init.sh
```

## Run

```bash
bash run.sh config.yml 
```

## Return mode

Set config.yml like

```yaml
port: 80
usessl: false
cert: ""
key: ""

route:
  default:
    mode: return
    content: a
```

## Proxy mode

Set config.yml like

```yaml
port: 80
usessl: false
cert: ""
key: ""

route:
  default:
    mode: proxy
    ssl: false
```

Set a url which you what to reverse in %systemroot%\System32\drivers\etc\hosts
```
<your ip>	tw.yahoo.com(url which you what to reverse)
```
Then when you connet to https://tw.yahoo.com (url which you what to reverse) you can get all data in https without encryption
