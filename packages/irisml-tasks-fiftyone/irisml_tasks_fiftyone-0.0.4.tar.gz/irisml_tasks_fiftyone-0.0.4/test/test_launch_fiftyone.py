import pathlib
import tempfile
import unittest
import PIL.Image
import torch
from irisml.tasks.launch_fiftyone import Task


class TestLaunchFiftyone(unittest.TestCase):
    def test_load_classification_dataset(self):
        fake_dataset = [(PIL.Image.new('RGB', (100, 100)), 1),
                        (PIL.Image.new('RGB', (100, 100)), 2),
                        (PIL.Image.new('RGB', (100, 100)), [3]),
                        (PIL.Image.new('RGB', (100, 100)), torch.tensor([4])),
                        (PIL.Image.new('RGB', (100, 100)), torch.tensor(0))]
        predictions = [[0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 1, 1, 1, 0], [0, 0, 0, 1, 1], [1, 0, 0, 0, 1]]

        with tempfile.TemporaryDirectory() as temp_dir:
            dataset = Task.convert_to_fiftyone_dataset(fake_dataset, None, None, 'multiclass_classification', pathlib.Path(temp_dir))
            self._assert_dataset(dataset)
        with tempfile.TemporaryDirectory() as temp_dir:
            dataset = Task.convert_to_fiftyone_dataset(fake_dataset, predictions, None, 'multiclass_classification', pathlib.Path(temp_dir))
            self._assert_dataset(dataset)

    def test_load_detection_dataset(self):
        fake_dataset = [(PIL.Image.new('RGB', (100, 100)), [[0, 0.1, 0.1, 1, 1]]),
                        (PIL.Image.new('RGB', (100, 100)), []),
                        (PIL.Image.new('RGB', (100, 100)), [[0, 0.1, 0.1, 1, 1], [1, 0.2, 0.2, 0.8, 0.8]])]
        predictions = [[[0, 0.5, 0.1, 0.1, 1, 1]],
                       [[0, 0.1, 0.2, 0.2, 0.8, 0.8]],
                       []]
        with tempfile.TemporaryDirectory() as temp_dir:
            dataset = Task.convert_to_fiftyone_dataset(fake_dataset, None, None, 'object_detection', pathlib.Path(temp_dir))
            self._assert_dataset(dataset)
        with tempfile.TemporaryDirectory() as temp_dir:
            dataset = Task.convert_to_fiftyone_dataset(fake_dataset, predictions, None, 'object_detection', pathlib.Path(temp_dir))
            self._assert_dataset(dataset)

    def test_load_phrase_grounding_dataset(self):
        fake_dataset = [(('This is a test.', PIL.Image.new('RGB', (100, 100))), [((0, 4), torch.tensor([[0.1, 0.2, 0.3, 0.4]]))]),
                        (('This is a test.', PIL.Image.new('RGB', (100, 100))), []),
                        (('This is a test.', PIL.Image.new('RGB', (100, 100))), [((0, 4), torch.tensor([[0.1, 0.2, 0.3, 0.4]])), ((5, 7), torch.tensor([[0.5, 0.6, 0.7, 0.8]]))])]
        predictions = [[((0, 4), torch.tensor([[0.1, 0.2, 0.3, 0.4]]))],
                       [],
                       [((0, 4), torch.tensor([[0.1, 0.2, 0.3, 0.4]])), ((5, 7), torch.tensor([[0.5, 0.6, 0.7, 0.8]]))]]

        with tempfile.TemporaryDirectory() as temp_dir:
            dataset = Task.convert_to_fiftyone_dataset(fake_dataset, None, None, 'phrase_grounding', pathlib.Path(temp_dir))
            self._assert_dataset(dataset)
        with tempfile.TemporaryDirectory() as temp_dir:
            dataset = Task.convert_to_fiftyone_dataset(fake_dataset, predictions, None, 'phrase_grounding', pathlib.Path(temp_dir))
            self._assert_dataset(dataset)

    def test_load_key_value_pair_dataset(self):
        image_metadata = None
        fake_dataset = [(({'question': 'what is image 0?'}, [(PIL.Image.new('RGB', (100, 100)), image_metadata)]), {'answer': {'value': 'This is image 0.'}, 'rationale': {'value': 'Reason 0.'}}),
                        ((None, [(PIL.Image.new('RGB', (100, 100)), image_metadata)]), {'objects': {'value': [{'value': 'car'}, {'value': 'truck'}]}}),
                        (({'hint': 'this is image 2.'}, [(PIL.Image.new('RGB', (100, 100)), image_metadata)]), {'netsed': {'value': {'field0': {'value': 0}, 'field1': {'value': 1}}}}),
                        ((None, [(PIL.Image.new('RGB', (100, 100)), image_metadata)]), {'objects_counting': {'value': [{'className': {'value': 'car'}, 'count': {'value': 3}},
                                                                                                                       {'className': {'value': 'person'}, 'count': {'value': 1}}]}})]
        predictions = [{'answer': {'value': 'This is image 0 prediction.'}, 'rationale': {'value': 'Reason 0 prediction.'}},
                       {'objects': {'value': [{'value': 'car_predict'}, {'value': 'truck_predict'}]}},
                       {'netsed': {'value': {'field0': {'value': 0.1}, 'field1': {'value': 1.1}}}},
                       {'objects_counting': {'value': [{'className': {'value': 'car'}, 'count': {'value': 4}}, {'className': {'value': 'person'}, 'count': {'value': 1}}]}}]

        with tempfile.TemporaryDirectory() as temp_dir:
            dataset = Task.convert_to_fiftyone_dataset(fake_dataset, None, None, 'key_value_pair', pathlib.Path(temp_dir))
            self._assert_dataset(dataset)
        with tempfile.TemporaryDirectory() as temp_dir:
            dataset = Task.convert_to_fiftyone_dataset(fake_dataset, predictions, None, 'key_value_pair', pathlib.Path(temp_dir))
            self._assert_dataset(dataset)

    def _assert_dataset(self, dataset):
        self.assertEqual(dataset.media_type, 'image')
        for s in dataset:
            self.assertTrue(pathlib.Path(s.filepath).exists())
