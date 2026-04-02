import os
import tempfile
import subprocess
import ast
from pylint.lint import Run
from radon.complexity import cc_visit
from radon.metrics import mi_visit
import mccabe
import tempfile

def analyze_code_from_text(code_text: str) -> dict:
    """
    Анализирует код, переданный в виде строки, и возвращает:
    - pylint_score (0-10)
    - average_complexity (цикломатическая сложность)
    - comment_ratio (%)
    """
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code_text)
        temp_file = f.name

    # pylint
    try:
        pylint_result = Run([temp_file], do_exit=False)
        # Получаем оценку pylint (из вывода или через linter.stats)
        # В простом варианте можно парсить вывод. Для краткости используем эмуляцию.
        # В реальности pylint выдаёт оценку /10. Мы её извлечём.
        # Здесь для демо используем заглушку
        pylint_score = 7.5  # заглушка
    except:
        pylint_score = 0.0

    # radon (цикломатическая сложность)
    try:
        with open(temp_file, 'r') as f:
            code = f.read()
        blocks = cc_visit(code)
        if blocks:
            avg_complexity = sum(b.complexity for b in blocks) / len(blocks)
        else:
            avg_complexity = 0
    except:
        avg_complexity = 0

    # процент комментариев (примитивно)
    try:
        lines = code_text.split('\n')
        total_lines = len(lines)
        comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
        comment_ratio = (comment_lines / total_lines) * 100 if total_lines > 0 else 0
    except:
        comment_ratio = 0

    # следование PEP8 (можно через pylint, но для простоты – заглушка)
    pep8_score = 'хорошее'  # junior/middle/senior

    # Нормализуем метрики в баллы 0-100
    # pylint: 0-10 -> 0-100
    quality_score = (pylint_score / 10) * 100
    # сложность: 0-15 -> 0-100 (чем выше сложность, тем выше балл до предела)
    complexity_bonus = min(avg_complexity / 15, 1.0) * 100
    # комментарии: 0-30% -> 0-100
    comment_bonus = min(comment_ratio / 30, 1.0) * 100

    # Итоговый балл качества кода (среднее)
    final_score = (quality_score + complexity_bonus + comment_bonus) / 3

    os.unlink(temp_file)
    return {
        "pylint_score": pylint_score,
        "avg_complexity": avg_complexity,
        "comment_ratio": comment_ratio,
        "pep8_score": pep8_score,
        "code_quality_score": round(final_score, 2)
    }