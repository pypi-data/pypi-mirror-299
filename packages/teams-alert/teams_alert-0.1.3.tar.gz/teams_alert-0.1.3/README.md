# teams_alert

## Introduction

teams_alert is a python package that allows you to send alerts to Microsoft Teams. It is a simple package that allows you to send messages to a channel in Microsoft Teams.

## Getting Started

1. Installation process
```pip install teams_alert```

2. Import the package
```from teams_alert import TeamsAlert```

3. Get the webhook url from the channel in Microsoft Teams.

First, go to the Team and channel you are interested in posting to. Click the three dots next to the channel name and select "Workflows".

![Workflows](https://raw.githubusercontent.com/jimbo-p/AoC23/e6fceefdc962b867d264f822ea0c3dae286b3bed/teams_workflows.JPG)

Next, find "Post to a channel when a webhook request is received"

![Post to a channel when a webhook request is received](https://raw.githubusercontent.com/jimbo-p/AoC23/e6fceefdc962b867d264f822ea0c3dae286b3bed/teams_webhook_workflow.JPG)

Name the workflow if you so desire

![Name the workflow](https://raw.githubusercontent.com/jimbo-p/AoC23/e6fceefdc962b867d264f822ea0c3dae286b3bed/workflows_naming.JPG)

Check that the Team and Channel are correct

![Check that the Team and Channel are correct](https://raw.githubusercontent.com/jimbo-p/AoC23/e6fceefdc962b867d264f822ea0c3dae286b3bed/workflow_team_and_channel.JPG)

Hellz yes, you got the webhook URL

![Hellz yes, you got the webhook URL](https://raw.githubusercontent.com/jimbo-p/AoC23/e6fceefdc962b867d264f822ea0c3dae286b3bed/workflow_URL.JPG)
1. Create an instance of TeamsAlert
```teams_alert = TeamsAlert(webhook_url)```

2. Send a message - email is optional
```teams_alert.send("Some sort of title you'd want to use", "Some sort of message you'd want to send", "jimbo_p@oxy.com")```