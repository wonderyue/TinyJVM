class Object:
    def __init__(self, clazz):
        self.clazz = clazz
        self.fields = [None] * clazz.instance_field_count

    def is_instance_of(self, clazz) -> bool:
        return clazz.is_assignable_from(self.clazz)
