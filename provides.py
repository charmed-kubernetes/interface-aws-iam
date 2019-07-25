from charms.reactive import when, when_not
from charms.reactive import set_flag, clear_flag
from charms.reactive import Endpoint


# kubernetes-master side
class AWSIAMProvides(Endpoint):

    @when('endpoint.{endpoint_name}.changed')
    def changed(self):
        # we want to make sure all the templates and stuff are written
        # and pods started before we switch the API server over to
        # use the webhook. This is critical for the webhook template
        # since the API server will crash if the file isn't there.
        if all(unit.received['webhook_status']
               for unit in self.all_joined_units):
            set_flag(self.expand_name('endpoint.{endpoint_name}.ready'))
        set_flag(self.expand_name('endpoint.{endpoint_name}.available'))
        clear_flag('endpoint.{endpoint_name}.changed')

    @when_not('endpoint.{endpoint_name}.joined')
    def broken(self):
        clear_flag(self.expand_name('endpoint.{endpoint_name}.ready'))
        clear_flag(self.expand_name('endpoint.{endpoint_name}.available'))

    def get_cluster_id(self):
        if len(self.all_joined_units) > 0:
            return self.all_joined_units[0].received['cluster_id']
        else:
            return None

    def set_api_server_status(self, status):
        for relation in self.relations:
            relation.to_publish['api_server_state'] = status
