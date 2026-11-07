import unittest


def calcular_emisiones_carbono(consumo_kwh, factor_emision=0.4):
    """
    Calcula las emisiones de carbono a partir del consumo en kWh.
    Lanza ValueError si el consumo es negativo.
    """
    if consumo_kwh < 0:
        raise ValueError("El consumo de kWh no puede ser negativo.")

    return consumo_kwh * factor_emision


class TestCalculoEmisiones(unittest.TestCase):

    def test_calculo_nominal(self):
        # Validamos que 100 kWh * 0.4 = 40.0
        self.assertAlmostEqual(calcular_emisiones_carbono(100), 40.0)
        # Validamos con otro factor de emisión: 250 * 0.5 = 125.0
        self.assertAlmostEqual(calcular_emisiones_carbono(250, 0.5), 125.0)

    def test_consumo_cero(self):
        # Validamos que 0 kWh devuelve 0 emisiones
        self.assertEqual(calcular_emisiones_carbono(0), 0.0)

    def test_consumo_negativo_lanza_value_error(self):
        # Validamos que si el consumo es -10, lance una excepción ValueError
        with self.assertRaises(ValueError):
            calcular_emisiones_carbono(-10)


if __name__ == "__main__":
    unittest.main()