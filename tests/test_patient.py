"""Tests for the Patient model."""
import pytest
import numpy as np
from inflammation.models import Patient


@pytest.fixture()
def patient_1():
    return Patient(id = 1, data = [1,2,3,4,5])

@pytest.fixture()
def patient_2():
    return Patient(id = 2, data = [10,20,30,40,50])

class TestPatient:

    def test_patient_data_mean(self, patient_1):
        assert patient_1.data_mean() == 3.0

    def test_patient_data_max(self, patient_1):
        assert patient_1.data_max() == 5

    def test_patient_data_min(self, patient_1):
        assert patient_1.data_min() == 1

    def test_patient_attributes(self, patient_2):
        assert patient_2.id == 2
        assert patient_2.data == [10, 20, 30, 40, 50]

