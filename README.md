# aws-iam interface

This interface provides communication between kubernetes-master
and aws-iam subordinate

It allows the requires side, aws-iam, to know when the api server is
up and available and to tell the api server when the webhook.yaml
file is written so that it may restart and use the webhook.

## Provides (kubernetes-master side)

### States
 * `aws-iam.available`
   Indicates that there are one or more charms on the other side of the relation
 * `aws-iam.ready`
   Indicates that the webhook status has been set. This is used to indicate it is time
   to restart the API server to pick up the webhook config on the Kubernetes side.
### Methods
 * `get_cluster_id`
   The AWS-IAM charm generates a random cluster ID for the cluster that is needed
   in the kubectl configuration file. This is passed over the relation here.
 * `set_api_server_status`

## Requires (aws-iam side)

### States
 * `aws-iam.available`
   Indicates that there are one or more charms on the other side of the relation
### Methods
 * `set_cluster_id`
   The AWS-IAM charm generates a random cluster ID for the cluster that is needed
   in the kubectl configuration file. This is passed over the relation here.
 * `set_webhook_status`
   Called to set that the webhook configuration has been written to disk.