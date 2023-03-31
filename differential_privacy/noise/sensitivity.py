import numpy as np
import typing


class CalSensitivity:

    def __init__(self):
        pass

    @staticmethod
    def cal_ord_norm_sensitivity(sensitivities: typing.Iterable = None, ord: int = 2):
        """
        Args:
            sensitivities: An typing.Iterable consisting of the original sensitivities.
            ord: An int indicating to calculate ord-norm of sensitivities

        Returns:
            A tuple of sensitivities replaced by its ord-norm result
        """
        sens_arr = np.array(sensitivities)
        sens_arr_not_none = sens_arr[sens_arr != np.array(None)]
        norm_result = np.linalg.norm(sens_arr_not_none, ord=ord)
        sens_arr[sens_arr != np.array(None)] = norm_result
        return tuple(sens_arr)
