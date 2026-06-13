from pathlib import Path

import pandas as pd

from src.core.template import TemplateGenerator
from src.models.fields import STANDARD_FIELDS


def test_generate_csv_template(tmp_path: Path) -> None:
    output = tmp_path / "template.csv"
    result = TemplateGenerator().generate("csv", str(output))
    assert Path(result).exists()
    assert output.exists()
    desc_path = tmp_path / "template_字段说明.csv"
    assert desc_path.exists()

    frame = pd.read_csv(output)
    assert list(frame.columns) == STANDARD_FIELDS
    assert len(frame) == 2


def test_generate_csv_template_no_sample(tmp_path: Path) -> None:
    output = tmp_path / "template.csv"
    result = TemplateGenerator().generate("csv", str(output), with_sample=False)
    frame = pd.read_csv(output)
    assert list(frame.columns) == STANDARD_FIELDS
    assert len(frame) == 0


def test_generate_excel_template(tmp_path: Path) -> None:
    output = tmp_path / "template.xlsx"
    result = TemplateGenerator().generate("excel", str(output))
    assert Path(result).exists()
    assert output.exists()

    xls = pd.ExcelFile(output)
    assert "数据模板" in xls.sheet_names
    assert "字段说明" in xls.sheet_names

    data_frame = pd.read_excel(output, sheet_name="数据模板")
    assert list(data_frame.columns) == STANDARD_FIELDS
    assert len(data_frame) == 2

    desc_frame = pd.read_excel(output, sheet_name="字段说明")
    assert "字段名" in desc_frame.columns
    assert "字段说明" in desc_frame.columns
    assert "是否必填" in desc_frame.columns
    assert "类型" in desc_frame.columns
    assert len(desc_frame) == len(STANDARD_FIELDS)
