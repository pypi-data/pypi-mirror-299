import unittest
import torch
import PIL.Image
from irisml.tasks.create_torchvision_transform import Task


class TestCreateTorchvisionTransform(unittest.TestCase):
    def test_simple(self):
        config = Task.Config(["Resize((256, 256), 'InterpolationMode.BICUBIC')", "CenterCrop(224)", "RandomHorizontalFlip(0.1)", "ColorJitter(0.2, 0.2)"])
        outputs = Task(config).execute(Task.Inputs())

        image = PIL.Image.new('RGB', (500, 500))
        transformed = outputs.transform(image)

        self.assertIsInstance(transformed, torch.Tensor)
        self.assertEqual(transformed.shape, (3, 224, 224))

    def test_resize_down(self):
        config = Task.Config(["ResizeDown(768, max_size=2048)"])
        outputs = Task(config).execute(Task.Inputs())

        image = PIL.Image.new('RGB', (4000, 1000))
        transformed = outputs.transform(image)

        self.assertIsInstance(transformed, torch.Tensor)
        self.assertEqual(transformed.shape, (3, 512, 2048))
