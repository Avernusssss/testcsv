import argparse
import csv
import os
from abc import ABC, abstractmethod
from tabulate import tabulate

# --- Архитектурная часть: Базовый класс для отчетов ---

class Report(ABC):
    @abstractmethod
    def generate(self, data):
        pass

class PerformanceReport(Report):
    def generate(self, data):
        if not data:
            return []
        
        stats = {}
        for row in data:
            try:
                pos = row.get('position', '').strip()
                perf_str = row.get('performance', '').strip()
                
                if not pos or not perf_str:
                    continue
                    
                perf = float(perf_str)
                if pos not in stats:
                    stats[pos] = []
                stats[pos].append(perf)
            except (ValueError, KeyError) as e:
                continue
        
        if not stats:
            return []
        
        report_data = []
        for pos, perfs in stats.items():
            avg_perf = sum(perfs) / len(perfs)
            report_data.append([pos, round(avg_perf, 2)])
        
        report_data.sort(key=lambda x: x[1], reverse=True)
        return report_data


class ReportFactory:
    _reports = {
        "performance": PerformanceReport
    }

    @classmethod
    def get_report(cls, report_name):
        report_class = cls._reports.get(report_name.lower())
        if not report_class:
            raise ValueError(f"Отчет '{report_name}' не найден.")
        return report_class()


def load_data(file_paths):
    combined_data = []
    
    for path in file_paths:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Файл не найден: {path}")
        
        if not os.path.isfile(path):
            raise ValueError(f"Путь не является файлом: {path}")
        
        try:
            with open(path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                # Проверяем наличие обязательных колонок
                if not reader.fieldnames:
                    raise ValueError(f"Файл пустой или неверный формат: {path}")
                
                required_fields = {'position', 'performance'}
                if not required_fields.issubset(set(reader.fieldnames)):
                    missing = required_fields - set(reader.fieldnames)
                    raise ValueError(f"В файле {path} отсутствуют обязательные колонки: {missing}")
                
                rows = list(reader)
                if not rows:
                    print(f"Предупреждение: файл {path} не содержит данных")
                    continue
                    
                combined_data.extend(rows)
        except UnicodeDecodeError:
            raise ValueError(f"Ошибка кодировки файла: {path}. Убедитесь, что файл в кодировке UTF-8")
        except Exception as e:
            raise ValueError(f"Ошибка при чтении файла {path}: {e}")
    
    if not combined_data:
        raise ValueError("Не удалось загрузить данные из указанных файлов")
    
    return combined_data

def main():
    parser = argparse.ArgumentParser(
        description="Анализ эффективности разработчиков",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python analyser.py --files data1.csv data2.csv --report performance
  python analyser.py --files employees.csv --report performance
        """
    )
    parser.add_argument(
        "--files", 
        nargs='+', 
        required=True, 
        help="Пути к CSV файлам (можно указать несколько файлов через пробел)"
    )
    parser.add_argument(
        "--report", 
        required=True, 
        help="Название отчета (например, performance)"
    )
    
    args = parser.parse_args()

    try:
        # 1. Загрузка данных
        data = load_data(args.files)
        
        # 2. Получение нужного отчета через фабрику
        report_engine = ReportFactory.get_report(args.report)
        
        # 3. Генерация данных для отчета
        result = report_engine.generate(data)
        
        if not result:
            print("Нет данных для отображения.")
            return
        
        # 4. Вывод в консоль
        headers = ["Position", "Average Performance"]
        print(tabulate(result, headers=headers, tablefmt="grid"))
        
    except (FileNotFoundError, ValueError) as e:
        print(f"Ошибка: {e}")
        return 1
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    main()