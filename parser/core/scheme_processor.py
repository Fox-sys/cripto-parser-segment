class SchemeProcessor:
    def __int__(self):
        pass

    def process(self, response, scheme, token=None, single_target_mode=False):
        try:
            target_type = None
            scheme = scheme.replace(' ', '')
            path_to_list = ''
            print(1)
            if not single_target_mode:
                scheme = scheme.split('\n')[:2]
                if len(scheme) != 1:
                    path_to_list = scheme[0].replace('\r', '').split('->')
                path_to_object_name, target_type = scheme[-1].split(':')
                path_to_object_name = path_to_object_name.split('->')
            else:
                path_to_list = scheme.replace('\r', '').replace('\n', '').split('->')
            print(2)
            obj = response
            print(path_to_list)
            if path_to_list != '':
                for step in path_to_list:
                    if token == 'zzz':
                        print(obj)
                    try:
                        obj = obj[step.replace('{token}', str(token)) if token else step]
                    except TypeError:
                        obj = obj[int(step)]
            if target_type == 'dict' and not single_target_mode:
                obj = self.dict_post_process(obj, path_to_object_name)
            return obj
        except (KeyError, IndexError) as e:
            if token:
                print(e)
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
