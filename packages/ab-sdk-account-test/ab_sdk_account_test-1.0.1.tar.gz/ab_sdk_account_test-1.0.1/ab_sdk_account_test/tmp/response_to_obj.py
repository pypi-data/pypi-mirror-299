class ResponseToObj:

    def convert_snake_to_camel_case(self, text: str) -> str:
        camel_cased = "".join(x.capitalize() for x in text.lower().split("_"))
        if camel_cased:
            return camel_cased[0].lower() + camel_cased[1:]
        else:
            return camel_cased

    def get_type(self, value):
        if isinstance(value, int):
            return "int"
        elif isinstance(value, dict):
            return "dict"
        elif isinstance(value, str):
            return "str"
        elif isinstance(value, list):
            return "list"
        return "<><><><><><"

    def process(self, response):
        for key in response:
            value = response[key]
            camel_cased_key = self.convert_snake_to_camel_case(key)
            camel_cased_key = f"{camel_cased_key} : {self.get_type(value)} = None"
            if isinstance(value, dict):
                print("\n\n")
                print(camel_cased_key)
                print("-------------------------------- Start")
                self.process(value)
                print("-------------------------------- End")
                print("\n\n")
            if isinstance(value, list):
                print("-------------------------------- Start")
                self.process(value)
                print("-------------------------------- End")
                print("\n\n")
            else:
                print(camel_cased_key)
