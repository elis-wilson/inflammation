"""Module containing models representing patients and their data.

The Model layer is responsible for the 'business logic' part of the software.

Patients' data is held in an inflammation table (2D array) where each row contains 
inflammation data for a single patient taken over a number of days 
and each column represents a single day across all patients.
"""

import numpy as np

def daily_mean(data):
    """Calculate the daily mean of a 2d inflammation data array."""
    return np.mean(data, axis=0)


def daily_max(data):
    """Calculate the daily max of a 2d inflammation data array."""
    return np.max(data, axis=0)


def daily_min(data):
    """Calculate the daily min of a 2d inflammation data array."""
    return np.min(data, axis=0)

def patient_normalise(data):
    """Normalise patient data from a 2D inflammation data array."""

    if not isinstance(data, np.ndarray):
        raise TypeError('data input should be ndarray')
    if len(data.shape) != 2:
        raise TypeError('inflammation array should be 2-dimensional')
    if np.any(data < 0):
        raise ValueError('Inflammation values should not be negative')
    max_data = np.nanmax(data, axis=1)
    with np.errstate(invalid='ignore', divide='ignore'):
        normalised = data / max_data[:, np.newaxis]
    normalised[np.isnan(normalised)] = 0

    return normalised

class Patient:
    def __init__(self, id, data):
        self.id = id
        self.data = data

    @staticmethod
    def load_csv(filename):
        """Load a Numpy array from a CSV

        :param filename: Filename of CSV to load
        """
        return np.loadtxt(fname=filename, delimiter=',')


    def data_mean(self):
        """Calculate the daily mean of a 2d inflammation data array."""
        return np.mean(self.data)


    def data_max(self):
        """Calculate the daily max of a 2d inflammation data array."""
        return np.max(self.data)


    def data_min(self):
        """Calculate the daily min of a 2d inflammation data array."""
        return np.min(self.data)


class Trial:
    def __init__(self, data, id):
        self.data = data
        self.id = id

    def from_csv(cls, filename, id):
        data = cls.load_csv(filename)
        return(cls(data, id))

    @staticmethod
    def load_csv(filename):
        """Load a Numpy array from a CSV

        Parameters:
        filename (str). Filename of CSV to load
        """
        return np.loadtxt(fname=filename, delimiter=',')
    
    def get_patient(self, row):
        """Get a Patient object by data row. The id of the object is the
        same as the row number."""
        return Patient(row, self.data[row, :])

    def daily_mean(self):
        """Calculate the daily mean of a 2d inflammation data array."""
        return np.mean(self.data, axis=0)
    
    def daily_max(self):
        """Calculate the daily max of a 2d inflammation data array."""
        return np.max(self.data, axis=0)
    
    def daily_min(self):
        """Calculate the daily min of a 2d inflammation data array."""
        return np.min(self.data, axis=0)
        
    