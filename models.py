"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, designation, name, diameter, hazardous,  **info):
        """Create a new `NearEarthObject`.

        :param designation: Primary designation of a NEO
        :param name: IAU name (optional)
        :param diameter: diameter of NEO in kilometers (optional)
        :param hazardous: Whether the NEO is marked as hazardous to earth
        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self.designation = designation
        # Assigns name attribute
        if len(name):
            self.name = name
        else:
            self.name = None
        # Assigns diameter attribute
        if len(diameter):
            self.diameter = float(diameter)
        else:
            self.diameter = float('nan')
        # Assigns hazardous attribute
        if hazardous == 'Y':
            self.hazardous = True
        else:
            self.hazardous = False
        # Collection of close approaches associated with this NEO
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return f'{self.designation} ({self.name})'

    def __str__(self):
        """Return `str(self)`."""
        return f"NEO {self.fullname} has a diameter of {self.diameter} km and {'is' if self.hazardous else 'is not'} potentially hazardous"


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, designation, time, distance, velocity, **info):
        """Create a new `CloseApproach`.

        :param designation: The NEO's primary designation
        :param time: Date and time of the close approaches
        :param distance: Approach distance in astronomical units
        :param velocity: Relative approach velocity in kilometers per second
        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self._designation = designation
        self.time = cd_to_datetime(time)
        self.distance = float(distance)
        self.velocity = float(velocity)
        # NearEarthObject associated with this approach
        self.neo = None

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return f'{self._designation}: {self.neo}'

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        return f'At {self.time_str} NearEarthObject {self.fullname} approaches earth at a distance of {round(self.distance, 4) } au and a velocity of {round(self.velocity, 4)} km/s '

    def json_serialize(self):
        """Serialize a CloseApproach object into a dictionary for the write_to_json function."""
        json_dict = {'datetime_utc': self.time_str,
                     'distance_au': self.distance,
                     'velocity_km_s': self.velocity,
                     'neo': {
                            'designation': self.neo.designation,
                            'name': self.neo.name,
                            'diameter_km': self.neo.diameter,
                            'potentially_hazardous': self.neo.hazardous
                            }
                     }

        return json_dict

    def csv_serialize(self):
        """Serialize a CloseApproach object into a dictionary for the write_to_csv function."""
        csv_dict = {'datetime_utc': self.time_str,
                    'distance_au': self.distance,
                    'velocity_km_s': self.velocity,
                    'designation': self.neo.designation,
                    'name': self.neo.name,
                    'diameter_km': self.neo.diameter,
                    'potentially_hazardous': self.neo.hazardous
                    }

        return csv_dict
