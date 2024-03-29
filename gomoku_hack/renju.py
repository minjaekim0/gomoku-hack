from typing import List, Union
from abc import abstractmethod
import numpy as np
from copy import copy
from collections import defaultdict
from gomoku_hack.util import array_nan_equal


class Two4Checker:
    def __init__(self, board_calc: List[List[Union[int, None]]]) -> None:
        self.board_len = 15
        self.board_calc = board_calc
    
    def check_two_4(self, x: int, y: int) -> bool:
        r = self.board_len // 2 - y
        c = x + self.board_len // 2
        
        if self.board_calc[r][c] in (0, 1):
            return False
        
        results = dict()
        for dir_ in ["horizontal", "vertical", "diagonal_downward", "diagonal_upward"]:
            results[dir_] = getattr(self, f"_check_4_{dir_}")(self.board_calc, r, c)
        
        if sum(results.values()) >= 2:
            return True
        else:
            return False

    def _check_4_horizontal(self, board_calc, r, c) -> bool:
        board_copy = copy(board_calc)
        board_copy[r][c] = 1
        left_bound = max(0, c - 4)
        right_bound = min(self.board_len - 5, c)
        for b in range(left_bound, right_bound + 1):
            sum_subject = board_copy[r, b:b+5]
            
            if b > 1:
                left_of_subject = board_copy[r, b-1]
            else:
                left_of_subject = "out"
            if b < self.board_len - 5:
                right_of_subject = board_copy[r, b+5]
            else:
                right_of_subject = "out"
            
            if np.nansum(sum_subject) == 4 and \
                np.isnan(sum_subject).sum() == 1 and \
                left_of_subject != 1 and \
                right_of_subject != 1:
                return True
        return False
    
    def _check_4_vertical(self, board_calc, r, c) -> bool:
        transposed = board_calc.T
        return self._check_4_horizontal(transposed, c, r)
    
    def _check_4_diagonal_downward(self, board_calc, r, c) -> bool:
        board_copy = copy(board_calc)
        board_copy[r][c] = 1
        upperleft_available = min(r, c, 4)
        lowerright_available = min(self.board_len - r - 1, self.board_len - c - 1, 4)
        left_bound = c - upperleft_available
        upper_bound = r - upperleft_available
        right_bound = c + lowerright_available - 4
        lower_bound = r + lowerright_available - 4
        
        for b1, b2 in zip(range(upper_bound, lower_bound + 1), range(left_bound, right_bound + 1)):
            sum_subject = board_copy[b1:b1+5, b2:b2+5].diagonal()
            
            if b1 > 1 and b2 > 1:
                upperleft_of_subject = board_copy[b1-1, b2-1]
            else:
                upperleft_of_subject = "out"
            if b1 < self.board_len - 5 and b2 < self.board_len - 5:
                lowerright_of_subject = board_copy[b1+1, b2+5]
            else:
                lowerright_of_subject = "out"
                
            if np.nansum(sum_subject) == 4 and \
                np.isnan(sum_subject).sum() == 1 and \
                upperleft_of_subject != 1 and \
                lowerright_of_subject != 1:
                return True
        return False
    
    def _check_4_diagonal_upward(self, board_calc, r, c) -> bool:
        flipped = np.flipud(board_calc)
        return self._check_4_diagonal_downward(flipped, self.board_len - r - 1, c)


class TwoOpen3Checker:
    def __init__(self, board_calc: List[List[Union[int, None]]]) -> None:
        self.board_len = 15
        self.board_calc = board_calc

    def check_two_open3(self, x: int, y: int) -> bool:
        r = self.board_len // 2 - y
        c = x + self.board_len // 2
        
        if self.board_calc[r][c] in (0, 1):
            return False

        results = defaultdict(dict)
        for open3_type in ["spaced", "continuous"]:
            for dir_ in ["horizontal", "vertical", "diagonal_downward", "diagonal_upward"]:
                results[open3_type][dir_] = getattr(self, f"_check_open3_{open3_type}_{dir_}")(self.board_calc, r, c)
        
        if sum([sum(d.values()) for d in results.values()]) >= 2:
            return True
        else:
            return False

    def _check_open3_spaced_horizontal(self, board_calc, r, c) -> bool:
        board_copy = copy(board_calc)
        board_copy[r][c] = 1
        left_bound = max(0, c - 4)
        right_bound = min(self.board_len - 6, c - 1)
        
        for b in range(left_bound, right_bound + 1):
            subject = board_copy[r, b:b+6]
            
            if array_nan_equal(subject, [np.nan, 1, np.nan, 1, 1, np.nan]) or \
                array_nan_equal(subject, [np.nan, 1, 1, np.nan, 1, np.nan]):
                return True
        return False
    
    def _check_open3_spaced_vertical(self, board_calc, r, c) -> bool:
        transposed = board_calc.T
        return self._check_open3_spaced_horizontal(transposed, c, r)
    
    def _check_open3_spaced_diagonal_downward(self, board_calc, r, c) -> bool:
        board_copy = copy(board_calc)
        board_copy[r][c] = 1
        upperleft_available = min(r, c, 4)
        lowerright_available = min(self.board_len - r - 1, self.board_len - c - 1, 4)
        left_bound = c - upperleft_available
        upper_bound = r - upperleft_available
        right_bound = c + lowerright_available - 5
        lower_bound = r + lowerright_available - 5
        
        for b1, b2 in zip(range(upper_bound, lower_bound + 1), range(left_bound, right_bound + 1)):
            subject = board_copy[b1:b1+6, b2:b2+6].diagonal()
            
            if array_nan_equal(subject, [np.nan, 1, np.nan, 1, 1, np.nan]) or \
                array_nan_equal(subject, [np.nan, 1, 1, np.nan, 1, np.nan]):
                return True
        return False
    
    def _check_open3_spaced_diagonal_upward(self, board_calc, r, c) -> bool:
        flipped = np.flipud(board_calc)
        return self._check_open3_spaced_diagonal_downward(flipped, self.board_len - r - 1, c)

    def _check_open3_continuous_horizontal(self, board_calc, r, c) -> bool:
        board_copy = copy(board_calc)
        board_copy[r][c] = 1
        left_bound = max(0, c - 3)
        right_bound = min(self.board_len - 5, c - 1)
        
        for b in range(left_bound, right_bound + 1):
            subject = board_copy[r, b:b+5]
            
            if array_nan_equal(subject, [np.nan, 1, 1, 1, np.nan]):
                return True
        return False
    
    def _check_open3_continuous_vertical(self, board_calc, r, c) -> bool:
        transposed = board_calc.T
        return self._check_open3_continuous_horizontal(transposed, c, r)
    
    def _check_open3_continuous_diagonal_downward(self, board_calc, r, c) -> bool:
        board_copy = copy(board_calc)
        board_copy[r][c] = 1
        upperleft_available = min(r, c, 3)
        lowerright_available = min(self.board_len - r - 1, self.board_len - c - 1, 3)
        left_bound = c - upperleft_available
        upper_bound = r - upperleft_available
        right_bound = c + lowerright_available - 4
        lower_bound = r + lowerright_available - 4
        
        for b1, b2 in zip(range(upper_bound, lower_bound + 1), range(left_bound, right_bound + 1)):
            subject = board_copy[b1:b1+5, b2:b2+5].diagonal()
            
            if array_nan_equal(subject, [np.nan, 1, 1, 1, np.nan]):
                return True
        return False
    
    def _check_open3_continuous_diagonal_upward(self, board_calc, r, c) -> bool:
        flipped = np.flipud(board_calc)
        return self._check_open3_continuous_diagonal_downward(flipped, self.board_len - r - 1, c)


class MoreThan6Checker:
    def __init__(self, board_calc: List[List[Union[int, None]]]) -> None:
        self.board_len = 15
        self.board_calc = board_calc
    
    def check_more_than_6(self, x: int, y: int) -> bool:
        r = self.board_len // 2 - y
        c = x + self.board_len // 2
        
        if self.board_calc[r][c] in (0, 1):
            return False
        
        results = dict()
        for dir_ in ["horizontal", "vertical", "diagonal_downward", "diagonal_upward"]:
            results[dir_] = getattr(self, f"_check_6_{dir_}")(self.board_calc, r, c)
        
        if sum(results.values()) >= 1:
            return True
        else:
            return False

    def _check_6_horizontal(self, board_calc, r, c) -> bool:
        board_copy = copy(board_calc)
        board_copy[r][c] = 1
        left_bound = max(0, c - 5)
        right_bound = min(self.board_len - 6, c)
        for b in range(left_bound, right_bound + 1):
            subject = board_copy[r, b:b+6]
                        
            if subject.sum() == 6:
                return True
        return False
    
    def _check_6_vertical(self, board_calc, r, c) -> bool:
        transposed = board_calc.T
        return self._check_6_horizontal(transposed, c, r)
    
    def _check_6_diagonal_downward(self, board_calc, r, c) -> bool:        
        board_copy = copy(board_calc)
        board_copy[r][c] = 1
        upperleft_available = min(r, c, 5)
        lowerright_available = min(self.board_len - r - 1, self.board_len - c - 1, 5)
        left_bound = c - upperleft_available
        upper_bound = r - upperleft_available
        right_bound = c + lowerright_available - 5
        lower_bound = r + lowerright_available - 5
        
        for b1, b2 in zip(range(upper_bound, lower_bound + 1), range(left_bound, right_bound + 1)):
            subject = board_copy[b1:b1+6, b2:b2+6].diagonal()
            
            if sum(subject) == 6:
                return True
        return False
    
    def _check_6_diagonal_upward(self, board_calc, r, c) -> bool:
        flipped = np.flipud(board_calc)
        return self._check_6_diagonal_downward(flipped, self.board_len - r - 1, c)


class RenjuChecker(Two4Checker, TwoOpen3Checker, MoreThan6Checker):
    def __init__(self, board_calc: List[List[Union[int, None]]]) -> None:
        super().__init__(board_calc)
        super().__init__(board_calc)
        super().__init__(board_calc)
        self.board_len = 15
        self.board_calc = board_calc
    
    def check(self, x: int, y: int) -> bool:
        r = self.board_len // 2 - y
        c = x + self.board_len // 2
        
        if self.board_calc[r][c] in (0, 1):
            return False
        
        results = dict()
        for forbid_type in ["two_4", "two_open3", "more_than_6"]:
            results[forbid_type] = getattr(self, f"check_{forbid_type}")(x, y)
        
        if sum(results.values()) >= 1:
            return True
        else:
            return False
