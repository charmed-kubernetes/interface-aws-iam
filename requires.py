from charms.reactive import when, when_not
from charms.reactive import set_flag, clear_flag
from charms.reactive import Endpoint


# aws-iam side
class AWSIAMRequires(Endpoint):

    @when('endpoint.{endpoint_name}.changed')
    def changed(self):
        # kubectl is used to deploy the webhook pod. This means that
        # the api server needs to be up in order to do that. So we
        # wait until the cluster is up before trying.
        if all(unit.received['api_server_state']
               for unit in self.all_joined_units):
            set_flag(self.expand_name('endpoint.{endpoint_name}.available'))
        clear_flag('endpoint.{endpoint_name}.changed')

    @when_not('endpoint.{endpoint_name}.joined')
    def broken(self):
        clear_flag(self.expand_name('endpoint.{endpoint_name}.available'))

    def set_webhook_status(self, status):
        for relation in self.relations:
            relation.to_publish['webhook_status'] = status

    def set_cluster_id(self, id):
        for relation in self.relations:
            relation.to_publish['cluster_id'] = id
