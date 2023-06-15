from src.mlighter_utils.training import get_default_dataset, extract_xy_train, LoadDataOptions


class TestTraining:
    def test_get_default_dataset(self):
        df = get_default_dataset()
        assert df is not None
        assert df.iloc[137].tolist() == [6.4, 3.1, 5.5, 1.8, 'Iris-virginica']

    def test_get_default_dataset_with_numeric_labels(self):
        df = get_default_dataset(LoadDataOptions.WITH_NUMERIC)
        assert df is not None
        assert df.iloc[137].tolist() == [6.4, 3.1, 5.5, 1.8, 2]

    def test_extract_xy_train(self):
        x_train, y_train = extract_xy_train(get_default_dataset())
        assert x_train is not None
        assert y_train is not None
        assert len(x_train) == 120
        assert len(y_train) == 120
        assert x_train[0].tolist() == [6.4, 3.1, 5.5, 1.8]
        assert y_train[0] == 'Iris-virginica'
        assert x_train[3].tolist() == [6.1, 3.0, 4.9, 1.8]
        assert y_train[3] == 'Iris-virginica'
