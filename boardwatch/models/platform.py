class Platform():
    def __init__(self, name, is_brand_missing_from_name, platform_family_id, platform_family_name, model_no, storage_capacity, description, disambiguation, relevance, editions=[]):
        self.name = name
        self.is_brand_missing_from_name = is_brand_missing_from_name
        self.platform_family_id = platform_family_id
        self.platform_family_name = platform_family_name
        self.model_no = model_no
        self.storage_capacity = storage_capacity
        self.description = description
        self.disambiguation = disambiguation
        self.relevance = relevance
        self.editions = []
