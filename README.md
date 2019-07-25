# aws-iam interface

This interface provides communication between kubernetes-master
and aws-iam subordinate

It allows the requires side, aws-iam, to know when the api server is
up and available and to tell the api server when the webhook.yaml
file is written so that it may restart and use the webhook.
