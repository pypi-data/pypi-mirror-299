import ast
import dataclasses
from typing import Callable, List, Literal
import torch.nn
import torchvision.tv_tensors
import torchvision.transforms.v2
import irisml.core


class Task(irisml.core.TaskBase):
    """Create torchvision transform v2 object from string expressions.

    This task requires torchvision >= 0.15.

    This task creates a transform object in torchvision library from string expressions.
    The expression can be a simple method name such as "RandomCrop" or a method call such as "RandomCrop((32, 32))".

    ToDtype(torch.float32, scale=True) is always appended to the end of the transform.

    Example expressions:
    - "RandomCrop((32, 32))"
    - "Resize(224, 'InterpolationMode.BICUBIC')"

    Config:
        transforms ([str]): A list of transform descriptions.
        task_type (str): A task type. One of "classification_multiclass", "classification_multilabel", "image_text_classification", "object_detection", "phrase_grounding".
    """
    VERSION = '0.1.1'

    @dataclasses.dataclass
    class Config:
        transforms: List[str] = dataclasses.field(default_factory=list)
        task_type: Literal['classification_multiclass', 'classification_multilabel', 'image_text_classification', 'object_detection', 'phrase_grounding'] = 'classification_multiclass'

    @dataclasses.dataclass
    class Outputs:
        transform: Callable

    def execute(self, inputs):
        transform_configs = []
        for t in self.config.transforms:
            method_name, args = self._parse_transform(t)
            args = self._convert_known_param(args)
            if not hasattr(torchvision.transforms.v2, method_name):
                raise ValueError(f"torchvision.transforms.v2 doesn't have {method_name}")

            transform_class = getattr(torchvision.transforms.v2, method_name)
            if not issubclass(transform_class, torch.nn.Module):
                raise RuntimeError(f"{transform_class} has unexpected type.")

            transform_configs.append((method_name, args))

        transform = Transform(transform_configs, self.config.task_type)
        return self.Outputs(transform)

    def dry_run(self, inputs):
        return self.execute(inputs)

    @staticmethod
    def _parse_transform(expr):
        parsed = ast.parse(expr)
        if len(parsed.body) != 1:
            raise ValueError(f"Transform description cannot have multiple expressions: {expr}")

        if isinstance(parsed.body[0].value, ast.Name):
            return parsed.body[0].value.id, []
        elif isinstance(parsed.body[0].value, ast.Call):
            method_name = parsed.body[0].value.func.id
            ast_args = parsed.body[0].value.args
            args = []
            for arg in ast_args:
                if isinstance(arg, ast.Tuple):
                    if not all(isinstance(a, ast.Constant) for a in arg.elts):
                        raise ValueError(f"Only simple types are supported: {ast.dump(arg)}")
                    args.append(tuple(a.value for a in arg.elts))
                elif isinstance(arg, ast.Constant):
                    args.append(arg.value)
                else:
                    raise ValueError(f"Only simple types such as a number, a string, a tuple can be used as arguments: {ast.dump(arg)}")

            return method_name, args
        else:
            raise ValueError(f"Unexpected transform description: {ast.dump(parsed)}")

    @staticmethod
    def _convert_known_param(args):
        new_args = []
        for a in args:
            if a == 'InterpolationMode.NEAREST':
                a = torchvision.transforms.InterpolationMode.NEAREST
            elif a == 'InterpolationMode.NEAREST_EXACT':
                a = torchvision.transforms.InterpolationMode.NEAREST_EXACT
            elif a == 'InterpolationMode.BILINEAR':
                a = torchvision.transforms.InterpolationMode.BILINEAR
            elif a == 'InterpolationMode.BICUBIC':
                a = torchvision.transforms.InterpolationMode.BICUBIC
            new_args.append(a)
        return new_args


class Transform:
    def __init__(self, transform_configs: List, task_type: str):
        transform_instances = [torchvision.transforms.v2.ToImage()]
        for method_name, args in transform_configs:
            transform_class = getattr(torchvision.transforms.v2, method_name)
            transform_instances.append(transform_class(*args))
        transform_instances.append(torchvision.transforms.v2.ToDtype(torch.float32, scale=True))
        self._transform = torchvision.transforms.v2.Compose(transform_instances)
        self._transform_configs = transform_configs
        self._task_type = task_type

    def __call__(self, inputs, targets):
        if self._task_type in ('classification_multiclass', 'classification_multilabel'):
            assert isinstance(targets, torch.Tensor) and targets.dim() in (0, 1)
            return self._transform(inputs), targets
        elif self._task_type == 'object_detection':
            assert isinstance(targets, torch.Tensor) and targets.dim() == 2 and targets.shape[1] == 5
            boxes = torchvision.tv_tensors.BoundingBoxes(targets[:, 1:], format='XYXY', canvas_size=(1, 1))
            image, boxes = self._transform(inputs, boxes)
            targets = torch.cat((targets[:, 0:1], boxes), dim=1)
            targets = targets[torch.logical_and(targets[:, 1] < targets[:, 3], targets[:, 2] < targets[:, 4])]  # Some boxes may be removed by the transform
            targets[:, 1] /= image.shape[2]
            targets[:, 2] /= image.shape[1]
            targets[:, 3] /= image.shape[2]
            targets[:, 4] /= image.shape[1]
            return image, targets
        elif self._task_type == 'phrase_grounding':
            caption, image = inputs
            groundings = [(span, torchvision.tv_tensors.BoundingBoxes(boxes, format='XYXY', canvas_size=(1, 1))) for span, boxes in targets]
            image, groundings = self._transform(image, groundings)
            groundings = [(span, boxes[torch.logical_and(boxes[:, 0] < boxes[:, 2], boxes[:, 1] < boxes[:, 3])]) for span, boxes in groundings]
            groundings = [(span, boxes) for span, boxes in groundings if len(boxes) > 0]
            for _, boxes in groundings:
                boxes[:, 0] /= image.shape[2]
                boxes[:, 1] /= image.shape[1]
                boxes[:, 2] /= image.shape[2]
                boxes[:, 3] /= image.shape[1]

            return (caption, image), groundings
        elif self._task_type == 'image_text_classification':
            image, text = inputs
            return (self._transform(image), text), targets
        else:
            raise ValueError(f"Unknown task type: {self._task_type}")

    def __getstate__(self):
        return {'transform_configs': self._transform_configs, 'task_type': self._task_type}

    def __setstate__(self, state):
        self.__init__(**state)
