class SchemeProcessor:
    def __int__(self):
        pass

    def process(self, response: dict, scheme, token=None, single_target_mode=False):
        try:
            target_type = None
            scheme = scheme.replace(' ', '')
            path_to_list = ''
            if not single_target_mode:
                scheme = scheme.split('\n')[:2]
                if len(scheme) != 1:
                    path_to_list = scheme[0].replace('\r', '').split('->')
                path_to_object_name, target_type = scheme[-1].split(':')
                path_to_object_name = path_to_object_name.split('->')
            else:
                path_to_list = scheme.replace('\r', '').replace('\n', '').split('->')
            obj = response
            if path_to_list != '':
                for step in path_to_list:
                    try:
                        obj = obj[step.replace('{token}', str(token)) if token else step]
                    except TypeError:
                        obj = obj[int(step)]
            if single_target_mode:
                return obj
            if target_type == 'dict':
                obj = self.dict_post_process(obj, path_to_object_name)
            if target_type == 'key':
                obj = list(obj.keys())
            return obj
        except (KeyError, IndexError) as e:
            if token:
                return None
            raise e

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SchemeProcessor, cls).__new__(cls)
        return cls.instance

    def dict_post_process(self, pairs: list, path_to_object_name):
        pair_list = []
        for pair in pairs:
            obj = pair
            for step in path_to_object_name:
                obj = obj[step]
            pair_list.append(obj)
        return pair_list
