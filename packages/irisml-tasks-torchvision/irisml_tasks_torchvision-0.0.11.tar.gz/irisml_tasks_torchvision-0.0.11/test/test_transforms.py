import pytest
from PIL import Image
from irisml.tasks.create_torchvision_transform import ResizeDown, ResizeUp


class TestTransforms:
    @pytest.mark.parametrize("size,max_size,input_output_size_pairs", [
        (768, None, [
            ((128, 256), (128, 256)),
            ((1000, 1000), (768, 768)),
            ((1000, 4000), (768, 3072))
        ]),
        ((1024, 768), None, [
            ((128, 256), (128, 256)),
            ((128, 800), (128, 768)),
            (((2000, 800), (1024, 768)))
        ]),
        (768, 2048, [
            ((128, 256), (128, 256)),
            ((1000, 1000), (768, 768)),
            ((1000, 4000), (512, 2048))
        ]),
    ])
    def test_resize_down(self, size, max_size, input_output_size_pairs):
        transform = ResizeDown(size, max_size=max_size)
        for img_size, expected_size in input_output_size_pairs:
            img = Image.new("RGB", (img_size[1], img_size[0]))
            resized_img = transform(img)
            assert resized_img.size == (expected_size[1], expected_size[0])

    @pytest.mark.parametrize("size,max_size,input_output_size_pairs", [
        ((50, 60), None, [
            ((35, 40), (50, 60)),
            ((140, 150), (140, 150)),
            ((40, 80), (50, 80)),
            ((80, 40), (80, 60)),
        ]),
        ((60, 50), None, [
            ((35, 40), (60, 50)),
            ((140, 150), (140, 150)),
            ((40, 80), (60, 80)),
            ((80, 40), (80, 50)),
        ]),
        (50, 80, [
            ((35, 40), (50, 57)),
            ((40, 35), (57, 50)),
            ((40, 80), (40, 80)),
            ((80, 40), (80, 40)),
            ((40, 85), (40, 85)),
            ((85, 40), (85, 40)),
            ((140, 150), (140, 150)),
            ((150, 140), (150, 140)),
            ((10, 100), (10, 100)),
            ((100, 10), (100, 10)),
            ((55, 70), (55, 70)),
            ((70, 55), (70, 55))
        ]),
        (50, None, [
            ((35, 40), (50, 57)),
            ((40, 35), (57, 50)),
            ((40, 80), (50, 100)),
            ((80, 40), (100, 50)),
            ((140, 150), (140, 150)),
            ((150, 140), (150, 140)),
            ((10, 100), (50, 500)),
            ((100, 10), (500, 50))
        ])
    ])
    def test_resize_up(self, size, max_size, input_output_size_pairs):
        transform = ResizeUp(size, max_size=max_size)
        for img_size, expected_size in input_output_size_pairs:
            img = Image.new("RGB", (img_size[1], img_size[0]))
            resized_img = transform(img)
            assert resized_img.size == (expected_size[1], expected_size[0])
