import pandas as pd


def filter_by_words(operations: pd.DataFrame, search: str):
    """Функция для фильтрации дфтафрейма по ключевому слову.
    Возвращает операции в формате json"""
    if search is None:
        return operations
    else:
        filtered_df = operations[(operations['Категория'].str.contains(search, case=False)) &
                                 (operations['Описание'].str.contains(search, case=False))]
        json_answer = filtered_df.to_json()
        return json_answer
