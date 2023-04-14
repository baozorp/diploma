import pandas as pd
import numpy as np

# # Генерируем список случайных id
# ids = np.arange(2200)

# # Перемешиваем индексы
# shuffled_indices = np.random.permutation(2200)

# # Создаем DataFrame, используя перемешанные индексы в столбце "ID"
# df = pd.DataFrame(ids[shuffled_indices], columns=["ID"])

# # Сохраняем результат в файл без индексов
# df.to_csv('/Users/baozorp/Projects/Python/Diploma/results/heuristic.csv', index=False)


def interference_to_euristic(path):

    # загрузка файлов
    heuristic_df = pd.read_csv(path + '/heuristic.csv')
    recommendations_df = pd.read_csv(path + '/merged_recommendations.csv')

    heuristic_df = heuristic_df[heuristic_df['ID'].isin(recommendations_df['ID'])].reset_index(drop=True)
    # Выдаем очки для результатов эвристики
    max_score = recommendations_df['merge_scores'].max()
    num_rows = heuristic_df.shape[0]

    heuristic_df['heuristic_scores'] = heuristic_df.index.map(lambda i: (num_rows - i) * max_score / num_rows)

    merged_df = pd.merge(heuristic_df, recommendations_df, on='ID')

    merged_df['Optimal_Scores'] = merged_df[['merge_scores', 'heuristic_scores']].max(axis=1)

    merged_df = merged_df.drop(columns={'merge_scores', 'heuristic_scores'})

    sorted_df = merged_df.sort_values(by='Optimal_Scores', ascending=False)

    sorted_df.to_csv('/Users/baozorp/Projects/Python/Diploma/results/final_results.csv', index=False)

    # optimal_table = df2.set_index('ID').combine_first(df1.set_index('ID')).reset_index()
    # optimal_table.to_csv('/Users/baozorp/Projects/Python/Diploma/results/optimal_table.csv', index=False)
    # # создаем пустую таблицу для хранения результата
    # result = pd.DataFrame(columns=["ID"])

    # # инициализируем переменные для отслеживания индекса текущего элемента
    # idx1 = 0

    # # инициализируем переменные для отслеживания количества попыток поиска в каждой таблице
    # search_size1 = 10
    # search_size2 = 10
    # isNeedIncreaseFirstDF = True

    # while True:
    #     if len(df2) == 0:
    #         break
    #     # получаем текущий элемент из первой таблицы
    #     current_id = df1.iloc[idx1]["ID"]
    #     # bищем его среди первых search_size2 элементов второй таблицы
    #     matches = df2["ID"].iloc[:search_size2].isin([current_id]).values

    #     # если элемент найден, добавляем его в результат и удаляем из обеих таблиц
    #     if any(matches):
    #         indices = np.where(matches)[0]
    #         result = result.append(df2.iloc[indices[0]], ignore_index=True)
    #         df2_indices = df2.iloc[indices].index
    #         df1 = df1.drop(idx1).reset_index(drop=True)
    #         df2 = df2.drop(df2_indices).reset_index(drop=True)
    #         # Обновляем исходные данные
    #         idx1 = 0
    #         search_size1 = 10
    #         search_size2 = 10
    #         print(len(df2))
    #         continue

    #     if idx1 >= search_size1 and idx1 >= search_size2:
    #         idx1 = 0
    #         if isNeedIncreaseFirstDF:
    #             if search_size1 + 10 > len(df1):
    #                 search_size1 = len(df1)
    #             else:
    #                 search_size1 += 10
    #         else:
    #             if search_size2 + 10 > len(df2):
    #                 search_size2 = len(df2)
    #             else:
    #                 search_size2 += 10
    #         continue

    #     idx1 += 1
    # print(1)


interference_to_euristic('/Users/baozorp/Projects/Python/Diploma/results')
