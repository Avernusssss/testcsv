import pytest
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from analyser import PerformanceReport, ReportFactory, load_data

def test_performance_report_logic():
    sample_data = [
        {'position': 'Backend', 'performance': '5.0'},
        {'position': 'Backend', 'performance': '4.0'},
        {'position': 'Frontend', 'performance': '3.0'}
    ]
    report = PerformanceReport()
    result = report.generate(sample_data)
    
    assert result[0] == ['Backend', 4.5]
    assert result[1] == ['Frontend', 3.0]
    assert result[0][1] > result[1][1]

def test_performance_report_empty_data():
    report = PerformanceReport()
    result = report.generate([])
    assert result == []

def test_performance_report_single_position():
    sample_data = [
        {'position': 'Backend', 'performance': '5.0'},
        {'position': 'Backend', 'performance': '4.0'},
        {'position': 'Backend', 'performance': '6.0'}
    ]
    report = PerformanceReport()
    result = report.generate(sample_data)
    assert len(result) == 1
    assert result[0] == ['Backend', 5.0]

def test_performance_report_rounding():
    sample_data = [
        {'position': 'Backend', 'performance': '5.0'},
        {'position': 'Backend', 'performance': '4.0'},
        {'position': 'Backend', 'performance': '3.0'}
    ]
    report = PerformanceReport()
    result = report.generate(sample_data)
    assert result[0][1] == 4.0

def test_performance_report_invalid_data():
    sample_data = [
        {'position': 'Backend', 'performance': '5.0'},
        {'position': '', 'performance': '4.0'},
        {'position': 'Frontend', 'performance': ''},
        {'position': 'QA', 'performance': 'invalid'},
    ]
    report = PerformanceReport()
    result = report.generate(sample_data)
    assert len(result) == 1
    assert result[0] == ['Backend', 5.0]

def test_report_factory_error():
    with pytest.raises(ValueError):
        ReportFactory.get_report("non_existent_report")

def test_report_factory_case_insensitive():
    report1 = ReportFactory.get_report("performance")
    report2 = ReportFactory.get_report("PERFORMANCE")
    report3 = ReportFactory.get_report("Performance")
    assert isinstance(report1, PerformanceReport)
    assert isinstance(report2, PerformanceReport)
    assert isinstance(report3, PerformanceReport)

def test_load_data_from_files():
    test_dir = Path(__file__).parent
    file1 = test_dir / "employees1.csv"
    file2 = test_dir / "employees2.csv"
    
    data = load_data([str(file1), str(file2)])
    assert len(data) > 0
    assert 'position' in data[0]
    assert 'performance' in data[0]

def test_load_data_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_data(["non_existent_file.csv"])

def test_load_data_empty_file():
    test_dir = Path(__file__).parent
    empty_file = test_dir / "empty.csv"
    
    empty_file.write_text("position,performance\n", encoding='utf-8')
    
    try:
        with pytest.raises(ValueError, match="Не удалось загрузить данные"):
            load_data([str(empty_file)])
    finally:
        if empty_file.exists():
            empty_file.unlink()