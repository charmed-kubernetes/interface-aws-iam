from charms.reactive import Endpoint
from charms.reactive import toggle_flag


# aws-iam side
class AWSIAMRequires(Endpoint):

    # called automagically before any decorated handlers, but after
    # flags are set
    def manage_flags(self):
        # kubectl is used to deploy the webhook pod. This means that
        # the api server needs to be up in order to do that. So we
        # wait until the cluster is up before trying.
        toggle_flag(self.expand_name('endpoint.{endpoint_name}.available'),
                    self.is_joined and all(unit.received['api_server_state']
                                           for unit in self.all_joined_units))

    def set_webhook_status(self, status):
        for relation in self.relations:
            relation.to_publish['webhook_status'] = status

    def set_cluster_id(self, id):
        for relation in self.relations:
            relation.to_publish['cluster_id'] = id
