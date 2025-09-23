# TO:DO Добавить также замену букв на цифры: Егор -> 5гор

import pandas as pd
import random

# Определяем соседние клавиши для русской раскладки
keyboard_neighbors = {
    'й': ['ц', 'ф'], 'ц': ['й', 'у', 'ы'], 'у': ['ц', 'к', 'г'], 'к': ['у', 'е', 'н'],
    'е': ['к', 'н', 'о'], 'н': ['е', 'г', 'о'], 'г': ['н', 'ш', 'р'], 'ш': ['г', 'щ', 'з'],
    'щ': ['ш', 'з', 'х'], 'з': ['щ', 'х', 'ъ'], 'х': ['з', 'ъ', 'ф'], 'ъ': ['х', 'ф', 'ы'],
    'ф': ['й', 'ъ', 'ы', 'я'], 'ы': ['ф', 'ц', 'в', 'а'], 'в': ['ы', 'а', 'п'], 'а': ['в', 'п', 'р'],
    'п': ['а', 'р', 'о'], 'р': ['п', 'о', 'л'], 'о': ['р', 'л', 'д'], 'л': ['о', 'д', 'ж'],
    'д': ['л', 'ж', 'э'], 'ж': ['д', 'э', 'ё'], 'э': ['ж', 'ё', 'ю'], 'ё': ['э', 'ю', 'б'],
    'я': ['ф', 'ч', 'с'], 'ч': ['я', 'с', 'м'], 'с': ['ч', 'м', 'и'], 'м': ['с', 'и', 'т'],
    'и': ['м', 'т', 'ь'], 'т': ['и', 'ь', 'б'], 'ь': ['т', 'б', 'ю'], 'б': ['ь', 'ю', 'ё'],
    'ю': ['б', 'ё', '.']
}


def add_typos(text, typo_prob=0.1, max_typos_per_word=2):
    """
    Добавляет опечатки в текст путем замены букв на соседние на клавиатуре

    Args:
        text (str): исходный текст
        typo_prob (float): вероятность опечатки для каждого символа (0-1)
        max_typos_per_word (int): максимальное количество опечаток в одном слове

    Returns:
        str: текст с опечатками
    """
    words = text.split()
    result_words = []

    for word in words:
        # Пропускаем слишком короткие слова
        if len(word) <= 2:
            result_words.append(word)
            continue

        word_chars = list(word)
        typo_count = 0

        for i in range(len(word_chars)):
            char = word_chars[i].lower()

            # Проверяем, нужно ли добавлять опечатку
            if (char in keyboard_neighbors and
                    random.random() < typo_prob and
                    typo_count < max_typos_per_word):

                # Выбираем случайного соседа
                neighbor = random.choice(keyboard_neighbors[char])

                # Сохраняем регистр
                if word_chars[i].isupper():
                    neighbor = neighbor.upper()

                word_chars[i] = neighbor
                typo_count += 1

        result_words.append(''.join(word_chars))

    return ' '.join(result_words)


def add_truncation(text, trunc_prob=0.1, max_truncated_chars=3, min_word_length=4):
    """
    Добавляет отсечение правой части слова с заданной вероятностью

    Args:
        text (str): исходный текст
        trunc_prob (float): вероятность отсечения для каждого подходящего слова (0-1)
        max_truncated_chars (int): максимальное количество отсекаемых символов
        min_word_length (int): минимальная длина слова для отсечения

    Returns:
        str: текст с отсеченными словами
    """
    words = text.split()
    result_words = []

    for word in words:
        # Пропускаем слова, которые слишком коротки для отсечения
        if len(word) < min_word_length:
            result_words.append(word)
            continue

        # Проверяем, нужно ли отсекать это слово
        if random.random() < trunc_prob:
            # Определяем сколько символов отсекать (от 1 до max_truncated_chars)
            # Но не более чем осталось бы min_word_length-1 символов
            max_possible_trunc = len(word) - (min_word_length - 1)
            actual_max_trunc = min(max_truncated_chars, max_possible_trunc)

            if actual_max_trunc > 0:
                trunc_chars = random.randint(1, actual_max_trunc)
                truncated_word = word[:-trunc_chars]
                result_words.append(truncated_word)
            else:
                result_words.append(word)
        else:
            result_words.append(word)

    return ' '.join(result_words)


def add_mid_deletion(text, deletion_prob=0.1, max_deletions_per_word=1, min_word_length=4):
    """
    Удаляет буквы в середине слова с заданной вероятностью

    Args:
        text (str): исходный текст
        deletion_prob (float): вероятность удаления для каждого подходящего слова (0-1)
        max_deletions_per_word (int): максимальное количество удалений в одном слове
        min_word_length (int): минимальная длина слова для удаления букв

    Returns:
        str: текст с удаленными буквами в словах
    """
    words = text.split()
    result_words = []

    for word in words:
        # Пропускаем слишком короткие слова
        if len(word) < min_word_length:
            result_words.append(word)
            continue

        word_chars = list(word)
        deletion_count = 0
        attempts = 0
        max_attempts = len(word) * 2  # чтобы избежать бесконечного цикла

        # Пытаемся сделать удаления, но не более max_deletions_per_word
        while deletion_count < max_deletions_per_word and attempts < max_attempts:
            attempts += 1

            # Выбираем случайную позицию в середине слова (исключая первую и последнюю буквы)
            if len(word_chars) > 2:
                pos = random.randint(1, len(word_chars) - 2)
            else:
                break  # слово слишком короткое для удаления в середине

            # Проверяем вероятность удаления
            if random.random() < deletion_prob:
                # Удаляем символ в выбранной позиции
                deleted_char = word_chars.pop(pos)
                deletion_count += 1

                # Обновляем длину после удаления
                if len(word_chars) < min_word_length:
                    break  # остановиться, если слово стало слишком коротким

        result_words.append(''.join(word_chars))

    return ' '.join(result_words)

def augment_text(text, methods=None, **kwargs):
    """
    Универсальная функция для аугментации текста различными способами

    Args:
        text (str): исходный текст
        methods (list): список методов аугментации:
            - 'typos': опечатки
            - 'truncation': отсечение конца
            - 'mid_deletion': удаление в середине
        **kwargs: параметры для каждого метода

    Returns:
        str: аугментированный текст
    """
    if methods is None:
        methods = ['typos', 'truncation', 'mid_deletion']

    result = text

    if 'typos' in methods:
        result = add_typos(result, **kwargs)

    if 'truncation' in methods:
        result = add_truncation(result, **kwargs)

    if 'mid_deletion' in methods:
        result = add_mid_deletion(result, **kwargs)

    return result