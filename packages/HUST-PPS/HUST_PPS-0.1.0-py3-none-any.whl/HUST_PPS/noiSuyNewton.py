import numpy as np
import sympy as sp
import re

def TinhTySaiPhan(x: np.ndarray, y: np.ndarray):
    k = len(x) - 1
    zero_matrix = np.zeros((len(x), k + 2))
    zero_matrix[:, 0] = x
    zero_matrix[:, 1] = y
    cnt = 1
    for i in range(1, len(x)):
        index = i - 1
        for j in range(2, 2 + cnt):
            zero_matrix[i, j] = (zero_matrix[i, j - 1] - zero_matrix[i - 1, j - 1]) / (x[i] - x[index])
            index -= 1
        cnt += 1
    return zero_matrix

class Term:
    def __init__(self, coefficient, factors):
        self.coefficient = coefficient
        self.factors = factors

    def __str__(self):
        if len(self.factors) == 0:
            return str(self.coefficient)
        factors_str = '*'.join(f'(X - {factor})' for factor in self.factors)
        if self.coefficient == 1:
            return factors_str
        elif self.coefficient == -1:
            return f'-{factors_str}'
        else:
            return f'{self.coefficient}*{factors_str}'

class Polynomial:
    def __init__(self):
        self.terms = []

    def add_term(self, coefficient, factors):
        self.terms.append(Term(coefficient, factors))

    def __str__(self):
        return ' + '.join(str(term) for term in self.terms).replace('+ -', '- ')

def convert_to_float(value):
    # Trực tiếp kiểm tra các kiểu dữ liệu float và chuyển đổi
    if isinstance(value, (np.float64, np.float32, float)):
        return float(value)
    else:
        return value  # Không xử lý chuỗi hoặc các kiểu khác

# Thêm hàm chính để tạo đa thức Newton
def DaThucNoiSuyNewton(a: np.ndarray, b: np.ndarray):
    a = np.array([convert_to_float(ai) for ai in a])
    b = np.array([convert_to_float(bi) for bi in b])
    
    polynomial = Polynomial()
    polynomial.add_term(b[0], [])
    
    zero_matrix = TinhTySaiPhan(a, b)
    
    for i in range(1, len(a)):
        coefficient = zero_matrix[i, i+1]
        factors = a[:i].tolist()  # Convert NumPy array to list
        polynomial.add_term(coefficient, factors)
    
    # Simplify the final polynomial expression
    simplified_polynomial = sp.simplify(str(polynomial))  # Convert polynomial to string and simplify
    
    return polynomial, simplified_polynomial