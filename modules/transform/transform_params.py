class TransformParams:
    def __init__(self, data):
        self.transform_type = data.get('transform')
        self.image_path = data.get('image_path')
        self.params = data.get('params', {})
        self.p = self.params.get('p', 1.0)
        self.limit = self.params.get('limit', 90)
        self.blur = self.params.get('blur', 0)
        self.sharpen = self.params.get('sharpen', 0)
        self.brightness = self.params.get('brightness', 1.0)
        self.contrast = self.params.get('contrast', 1.0)
        self.noise = self.params.get('noise', 0)
