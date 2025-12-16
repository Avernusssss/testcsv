# Анализатор эффективности разработчиков

Программа для анализа эффективности разработчиков на основе CSV файлов. Использует паттерны Factory и Strategy для расширяемости.

## Использование

python analyser.py --files employees1.csv employees2.csv --report performance

CSV файлы должны содержать колонки `position` и `performance`. Программа выводит таблицу со средней эффективностью по каждой позиции, отсортированную по убыванию.

## Добавление нового типа отчета

1. Создайте класс, наследующийся от `Report`:
class CountReport(Report):
    def generate(self, data):
        # Ваша логика обработки данных
        return result

2. Зарегистрируйте в `ReportFactory._reports`:
_reports = {
    "performance": PerformanceReport,
    "count": CountReport  # новый отчет
}

Теперь можно использовать: `--report count`

## Тестирование

pytest tests/test_reports.py -v

<img width="950" height="690" alt="изображение" src="https://github.com/user-attachments/assets/0b1c8eeb-8478-440d-a273-ae45ef7826b1" />
