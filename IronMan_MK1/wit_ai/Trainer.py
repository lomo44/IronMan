from wit import *
import json
import re

class Trainer(Wit):

    def get_all_entities(self):
        return wit.req(self.logger, self.access_token, 'GET', '/entities', {})

    def get_entity_info(self, entity):
        return wit.req(self.logger, self.access_token, 'GET', '/entities/{0}'.format(entity), {})

    def add_entity(self, entity):
        # https://wit.ai/docs/http/20170307#post--entities-link
        print(wit.req(self.logger, self.access_token, 'POST', '/entities', {}, data=json.dumps(entity)))

    def update_entity(self, entity, update_info):
        # https://wit.ai/docs/http/20170307#put--entities-:entity-id-link
        # replace current value
        # cannot update lookup strategy
        print(wit.req(self.logger, self.access_token, 'PUT', '/entities/{0}'.format(entity), {}, data=json.dumps(update_info)))

    def add_value(self, entity, new_val):
        # https://wit.ai/docs/http/20170307#post--entities-:entity-id-values-link
        # Add a possible value into the list of values for the keyword entity.
        # will not erase old values
        print(wit.req(self.logger, self.access_token, 'POST', '/entities/{0}/values'.format(entity), {}, data=json.dumps(new_val)))


    def add_expression(self, entity, value, expression):
        # https://wit.ai/docs/http/20170307#post--entities-:entity-id-values-:value-id-expressions-link
        print(
        wit.req(self.logger, self.access_token, 'POST', '/entities/{0}/values/{1}/expressions'.format(entity, value),
                {}, data=json.dumps({'expression': expression})))

    def delete_entity(self, entity):
        print(wit.req(self.logger, self.access_token, 'DELETE', '/entities/{0}'.format(entity), {}))

    def add_samples(self, samples):
        # https://wit.ai/docs/http/20170307#post--samples-link
        print(wit.req(self.logger, self.access_token, 'POST', '/samples', {}, data=json.dumps(samples)))

    def add_file(self, file_name):
        with open(file_name) as json_data:
            d = json.load(json_data)
            for sample in d:
                for entity in sample['entities']:
                    try:
                        self.add_entity({'id': entity['entity']})
                    except:
                        print(entity['entity'] + ' is already added')
            self.add_samples(d)
        print('file added')

    def clean_up(self):
        entities = self.get_all_entities()
        for entity in entities:
            try:
                self.delete_entity(entity)
            except:
                break

    def init_entity(self, input_json_file):
        # import entities from Json file
        self.clean_up()
        with open(input_json_file) as json_in:
            init_data = json.load(json_in)
            exist_entities = self.get_all_entities()
            for new_entity in init_data:
                if new_entity['id'] not in exist_entities:
                    self.add_entity(new_entity)
                else:
                    self.update_entity(new_entity['id'], new_entity)

