from sage.all import *
import random as rd
import hashlib
from itertools import combinations, permutations
from Niederreiter import Niederreiter
from DataCollecctionScript import *
from math import factorial as fc

def remove_duplicates(nested_list):
    unique_list = []  # Пустой список
    for element in nested_list:
        if element not in unique_list:  # Проверяем каждый элемент
            unique_list.append(element)  # Добавляем, если элемент уникален
    return unique_list


def seconds_to_timestamp(seconds):
    """
    Преобразует количество секунд в строку формата HH:MM:SS.
    
    Параметры:
    seconds (int): Количество секунд (неотрицательное целое число).
    
    Возвращает:
    str: Строка в формате HH:MM:SS.
    
    Примеры:
    >>> seconds_to_timestamp(3661)
    '01:01:01'
    >>> seconds_to_timestamp(90000)
    '25:00:00'
    """
    if not isinstance(seconds, int) or seconds < 0:
        raise ValueError("Секунды должны быть целым неотрицательным числом")
    
    hours = seconds // 3600
    remainder = seconds % 3600
    minutes = remainder // 60
    seconds = remainder % 60
    
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def ISD(H, s, t, m1, v, l):
    n = H.ncols()
    k = n - H.nrows()
    # print("test", s.ncols())
    st = vector(GF(2), [s[i][0] for i in range(s.nrows())])
    
    info_sets = list(
        combinations(
                list(range(n)),
                k
            )
        )
    # shuffle(info_sets)
    indicator = 0
    # print(n,k)

    errors = []

    print(len(info_sets))

    # while True: pass

    for I in info_sets:
        I = sorted(list(I))
        J = sorted(
            list(
            set(range(n))-set(I)
            )
        )

        HI = Matrix(GF(2),
                    [H.column(i)
                     for i in I]
                    ).transpose()
        try:
            HI.inverse()
            
        except ZeroDivisionError:
            print(f"{indicator}/{len(info_sets)}")
            if len(errors)==120: print("FAIL")
            indicator += 1
            continue

        Zs = list(combinations(J, l))
        for Z in Zs:
            Z = sorted(list(Z))
            J_local = sorted(
                list(
                set(J)-set(Z)
                )
            )

            HZ = Matrix(GF(2),
                    [H.column(i)
                     for i in Z]
                    ).transpose()
            
            HJ = Matrix(GF(2),
                    [H.column(i)
                     for i in J_local]
                    ).transpose()
            
            # print(I,
            #       Z,
            #       J_local)
        
            UH_replaced = HZ.augment(HJ)
            UH_replaced = UH_replaced.augment(
                HI
            ).rref()

            U = Matrix(GF(2),
                       reversed(
                           [UH_replaced.column(-i)
                            for i in range(n-k)]
                       )).transpose()
            
            s1s2 = (s.transpose()*U.transpose())[0]
            s1 = s1s2[:l]
            s2 = s1s2[l:]

            AB = (UH_replaced.transpose()[
                HJ.ncols()+HZ.ncols():
            ]).transpose()

            A, B = AB[:l], AB[l:]

            X = list(combinations(I, m1))

            for x in X:
                S = []
                T = []

                y = list(set(I) - set(x))
                # print(x, y)
                # print()
                X_combinations = list(combinations(x, v))  # Все сочетания v элементов в X
                Y_combinations = list(combinations(y, v))  # Все сочетания v элементов в Y

                # Создание множества S
                S = []
                for positions in X_combinations:
                    exv = vector(GF(2), [1 if i in positions else 0 for i in range(k)])
                    a = exv * A.transpose()
                    S.append((a, exv))

                # Создание множества T
                T = []
                for positions in Y_combinations:
                    eyv = vector(GF(2), [1 if i in positions else 0 for i in range(k)])
                    a = s1 - eyv * A.transpose()  # s1 - eyv * A^T
                    T.append((a, eyv))

                # print(S)
                # print()
                # print(T)

                black_list = []

                for sp in S:
                    for tp in T:
                        ex = sp[1]
                        ey = tp[1]

                        # print(B*(ex+ey))
                        # print(s1)
                        wt = 0
                        col = s2+B*(ex+ey)
                        for i in range(col.length()):
                            if col[i]==1: wt += 1
                        if wt==t-2*v:
                            # print(ex+ey,
                            #       vector(GF(2),
                            #              [0]*l),
                            #              col)
                            ae = [0]*len(I+Z+J_local)

                            poses = I+Z+J_local
                            # print(set(poses))
                            # print("poses", len(poses))
                            tmp = list(ex+ey)+list(vector(GF(2), [0]*l))+list(col)
                            # print("tmp" , len(tmp))

                            for i, id in enumerate(poses):
                                ae[id] = int(tmp[i])
                            
                            # print(len(ae))

                            # while true: pass
                        

                            if vector(GF(2), ae) not in errors:
                                # print(vector(GF(2), ae), len(errors))
                                # while True: pass
                                # print(H*vector(GF(2), ae))
                                # print(st)
                                # print(type(H*vector(GF(2), ae))==type(st))
                                # while true: pass
                                if ae.count(1)==t and False:#H*vector(GF(2), ae)==st:
                                    return vector(GF(2), ae)
                                else: errors.append(vector(GF(2), ae))

                        # while True: pass
                        # if 
                        

                # while True: pass
        # while True: pass
        print(f"{indicator}/{len(info_sets)}")
        if len(errors)==120: print("FAIL")
        indicator += 1
        for err in errors:
            print(err)
        print()


#         I_m = []
#         for i in range(n):
#             tmp = []
#             for j in range(n):
#                 if i==j: tmp.append(1)
#                 else: tmp.append(0)
#             I_m.append(tmp)
#         shuffle(I_m)


# def partial_gaussian_elimination(H, l):
#     """
#     Приводит матрицу H к блочному виду с использованием частичного гауссова исключения.
#     Возвращает (H_new, permutation), где permutation — перестановка столбцов.
#     """
#     n = H.ncols()
#     m = H.nrows()
#     F = H.base_ring()
    
#     # Создаём расширенную матрицу [H | I]
#     H_aug = H.augment(matrix.identity(F, m), subdivide=True)
    
#     # Приводим к эшелонированной форме
#     H_ech = H_aug.echelon_form()
    
#     # Находим позиции ведущих элементов (пивотов) в левой части [H | I]
#     pivots = []
#     for row in H_ech.rows():
#         for idx, elem in enumerate(row[:n]):  # Игнорируем правый блок I
#             if elem != 0:
#                 pivots.append(idx)
#                 break
    
#     # Перестановка столбцов для перемещения пивотов в начало
#     permutation = list(range(n))
#     used_pivots = []
#     for i in range(min(m - l, len(pivots))):  # Первые (m-l) пивотов
#         p = pivots[i]
#         if p not in used_pivots:
#             permutation[i], permutation[p] = permutation[p], permutation[i]
#             used_pivots.append(p)
    
#     # Применяем перестановку к исходной матрице H
#     H_permuted = H[:, permutation]
    
#     # Дополнительное эшелонирование для обнуления элементов под диагональю
#     H_ech_final = H_permuted.echelon_form()
    
#     # Формируем блочную структуру [Id | A; 0 | B]
#     H_prime = block_matrix([
#         [H_ech_final[:m-l, :m-l], H_ech_final[:m-l, m-l:]],
#         [matrix(F, l, m-l), H_ech_final[m-l:, m-l:]]
#     ])
    
#     return H_prime, permutation


# def generate_error_vectors(length, weight, q):
#     """
#     Генерирует все векторы длины `length` с весом Хэмминга `weight` над полем GF(q).
#     """
#     vectors = []
#     for positions in combinations(range(length), weight):
#         vec = vector(GF(q), length)
#         for pos in positions:
#             vec[pos] = 1  # Для простоты, можно обобщить для GF(q)
#         vectors.append(vec)
#     return vectors

# def wagner_merge(L1, L2, u, q):
#     """
#     Объединяет два списка L1 и L2 по первым `u` позициям.
#     """
#     L1_sorted = sorted(L1, key=lambda x: tuple(x[1][:u]))
#     L2_sorted = sorted(L2, key=lambda x: tuple(x[1][:u]))
    
#     merged = []
#     i = j = 0
#     while i < len(L1_sorted) and j < len(L2_sorted):
#         x1 = L1_sorted[i][1]
#         x2 = L2_sorted[j][1]
#         sum_part = (x1[:u] + x2[:u]).change_ring(GF(q))
        
#         if sum_part.is_zero():
#             merged_e = vector(GF(q), L1_sorted[i][0].list() + L2_sorted[j][0].list())
#             merged_x = x1 + x2
#             merged.append((merged_e, merged_x))
#             i += 1
#             j += 1
#         elif tuple(x1[:u]) < tuple(x2[:u]):
#             i += 1
#         else:
#             j += 1
#     return merged

# def gba_niederreiter(H, s, t, a=1, q=2):
#     """
#     Обобщенная атака дней рождений для криптосистемы Нидеррайтера.
#     """
#     n, m = H.ncols(), H.nrows()
#     k = n - m
#     l = m // 2  # Эвристический выбор l
    
#     # Частичное гауссово исключение
#     H_prime, perm = partial_gaussian_elimination(H, l)
#     B = H_prime[-l:, - (k + l):]
#     s_prime = s * H_prime[:, perm].inverse()  # Корректировка синдрома
    
#     # Разделение синдрома
#     s2 = s_prime[-l:]
    
#     # Параметры для уровней
#     v = t  # Начальный вес (можно адаптировать)
#     split_factor = 2 ** a
#     block_size = (k + l) // split_factor
#     u = l // a  # Эвристический выбор u_i
    
#     # Генерация базовых списков
#     base_lists = []
#     for i in range(split_factor):
#         e_vectors = generate_error_vectors(block_size, v // split_factor, q)
#         B_block = B[:, i*block_size : (i+1)*block_size]
#         s_block = s2[i*(l//split_factor) : (i+1)*(l//split_factor)]
#         Li = [(e, e * B_block.T - s_block) for e in e_vectors]
#         base_lists.append(Li)
    
#     # Многоуровневое объединение
#     current_lists = base_lists
#     for level in range(a):
#         new_lists = []
#         for i in range(0, len(current_lists), 2):
#             merged = wagner_merge(current_lists[i], current_lists[i+1], u, q)
#             new_lists.append(merged)
#         current_lists = new_lists
    
#     # Проверка решений
#     for candidate in current_lists[0]:
#         e_combined = candidate[0]
#         if e_combined.hamming_weight() == t and e_combined * H.T == s:
#             # Восстановление исходной перестановки
#             e_full = vector(GF(q), n)
#             e_full[perm[- (k + l):]] = e_combined
#             return e_full
#     return None


def main():
    crypto = Niederreiter(4, 16, 2)
    print(crypto.public_key.nrows(),
          crypto.public_key.ncols())
    
    e = GetRandomMessageWithWeight(16, 2)
    print(e)

    print(e.ncols())

    s = crypto.H.transpose()*e.transpose()
    re = None

    e = vector(GF(2), [int(e[0][i]) for i in range(e.ncols())])

    count = 0
    # while re!=e:
    start = time.time()

    count += 1
    # params = {'l': 2, 'v': 1, 'u1': 3, 'u2': 2}
    re = ISD(crypto.H.transpose(), s, 2, 3, 1, 2)
    finish = int(time.time()-start)
    print(f"{re} - {e} is {re==e}")
    # print(finish)
    print(f"attempt {count}, time spent:{seconds_to_timestamp(finish)}")
    


if __name__=="__main__":
    main()