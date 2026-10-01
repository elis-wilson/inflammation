"""Tests for the Patient model."""
import pytest
import numpy as np
import numpy.testing as npt
from inflammation.models import Trial

#@pytest.fixture()
#def trial_instance():
#    return Trial("test_data.csv" , 1)

@pytest.fixture()
def trial_instance():
    return Trial(np.array([[0, 0],[0, 0]]), 1)

class TestTrial:

    def test_daily_mean_zeros(self, trial_instance):
        """Test that mean function works for an array of zeros."""
    
        test_result = np.array([0, 0])

        # Need to use Numpy testing functions to compare arrays
        npt.assert_array_equal(trial_instance.daily_mean(), test_result)


    def test_daily_mean_integers(self, trial_instance):
        """Test that mean function works for an array of positive integers."""
        
        trial_instance.data = np.array(
            [
            [1, 2],
            [3, 4],
            [5, 6]
            ]
            )
        test_result = np.array([3, 4])

        # Need to use Numpy testing functions to compare arrays
        npt.assert_array_equal(trial_instance.daily_mean(), test_result)


    def test_daily_min_string(self):
        """Test for TypeError when passing strings"""
        from inflammation.models import daily_min

        with pytest.raises(TypeError):
            error_expected = daily_min([['Hello', 'there'], ['General', 'Kenobi']])