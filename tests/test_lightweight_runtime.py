import unittest

from utils.preprocess import get_feature_input, preprocess
from utils.model_utils import predict, get_risk_level


class LightweightRuntimeTests(unittest.TestCase):
    def test_preprocess_accepts_plain_dict_input(self):
        row = get_feature_input(35, 12, 8, 450.0, 56.0, 90, "Silver", 2)
        self.assertIsInstance(row, dict)
        self.assertEqual(row["Membership"], 1)
        self.assertIn("Age", row)

    def test_predict_returns_probabilities_and_risk(self):
        model = {"weights": {"Age": -0.01, "Tenure_Months": -0.02, "Support_Calls": 0.08}}
        row = get_feature_input(35, 12, 8, 450.0, 56.0, 90, "Silver", 2)
        label, prob = predict(model, row)
        self.assertIn(label, (0, 1))
        self.assertGreaterEqual(prob, 0.0)
        self.assertLessEqual(prob, 1.0)
        risk_level, color = get_risk_level(prob)
        self.assertIn(risk_level, {"Low", "Medium", "High"})


if __name__ == "__main__":
    unittest.main()
