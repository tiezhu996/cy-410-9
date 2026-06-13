from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.models.fields import INTEGER_FIELDS, REQUIRED_FIELDS, STANDARD_FIELDS

FIELD_DESCRIPTIONS = {
    "project_name": "项目名称，必填项，非遗项目的正式名称",
    "project_code": "项目编号，必填项，项目的唯一标识符",
    "category": "项目类别，必填项，如传统技艺、传统美术等",
    "batch": "批次，数字类型，入选国家级/省级名录的批次",
    "region_province": "所在省份，必填项，项目所属省份",
    "region_city": "所在城市，项目所属地级市",
    "region_district": "所在区县，项目所属区县",
    "protection_unit": "保护单位，负责项目保护的单位名称",
    "inheritor_name": "传承人姓名，代表性传承人的姓名",
    "inheritor_age": "传承人年龄，数字类型，传承人的年龄",
    "inheritor_gender": "传承人性别，男/女",
    "endangerment": "濒危状况，如良好、一般、濒危等",
    "description": "项目描述，项目的简要介绍",
    "declare_year": "申报年份，数字类型，项目申报的年份",
}

SAMPLE_DATA = [
    {
        "project_name": "青瓷烧制技艺",
        "project_code": "H001",
        "category": "传统技艺",
        "batch": 2,
        "region_province": "浙江省",
        "region_city": "丽水市",
        "region_district": "龙泉市",
        "protection_unit": "龙泉青瓷保护中心",
        "inheritor_name": "张三",
        "inheritor_age": 58,
        "inheritor_gender": "男",
        "endangerment": "良好",
        "description": "传统青瓷烧制技艺，历史悠久",
        "declare_year": 2008,
    },
    {
        "project_name": "剪纸艺术",
        "project_code": "H002",
        "category": "传统美术",
        "batch": 1,
        "region_province": "江苏省",
        "region_city": "南京市",
        "region_district": "秦淮区",
        "protection_unit": "南京剪纸协会",
        "inheritor_name": "李四",
        "inheritor_age": 45,
        "inheritor_gender": "女",
        "endangerment": "一般",
        "description": "民间传统剪纸艺术",
        "declare_year": 2006,
    },
]


class TemplateGenerator:
    def generate(self, output_format: str, output_path: str, with_sample: bool = True) -> str:
        data_frame = self._build_data_frame(with_sample)
        desc_frame = self._build_description_frame()

        if output_format == "excel":
            return self._write_excel(data_frame, desc_frame, output_path)
        else:
            return self._write_csv(data_frame, desc_frame, output_path)

    def _build_data_frame(self, with_sample: bool) -> pd.DataFrame:
        if with_sample:
            return pd.DataFrame(SAMPLE_DATA, columns=STANDARD_FIELDS)
        return pd.DataFrame(columns=STANDARD_FIELDS)

    def _build_description_frame(self) -> pd.DataFrame:
        rows = []
        for field in STANDARD_FIELDS:
            required = "是" if field in REQUIRED_FIELDS else "否"
            field_type = "数字" if field in INTEGER_FIELDS else "文本"
            rows.append({
                "字段名": field,
                "字段说明": FIELD_DESCRIPTIONS.get(field, ""),
                "是否必填": required,
                "类型": field_type,
            })
        return pd.DataFrame(rows)

    def _write_excel(self, data_frame: pd.DataFrame, desc_frame: pd.DataFrame, output_path: str) -> str:
        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            data_frame.to_excel(writer, sheet_name="数据模板", index=False)
            desc_frame.to_excel(writer, sheet_name="字段说明", index=False)
            self._adjust_column_width(writer, "数据模板", data_frame)
            self._adjust_column_width(writer, "字段说明", desc_frame)
        return output_path

    def _adjust_column_width(self, writer, sheet_name: str, frame: pd.DataFrame) -> None:
        worksheet = writer.sheets[sheet_name]
        for idx, column in enumerate(frame.columns):
            max_length = max(
                frame[column].astype(str).map(len).max() if len(frame) > 0 else 0,
                len(str(column)),
            )
            worksheet.column_dimensions[chr(65 + idx)].width = min(max_length + 2, 40)

    def _write_csv(self, data_frame: pd.DataFrame, desc_frame: pd.DataFrame, output_path: str) -> str:
        path = Path(output_path)
        data_frame.to_csv(output_path, index=False, encoding="utf-8-sig")

        desc_path = path.with_name(f"{path.stem}_字段说明{path.suffix}")
        desc_frame.to_csv(desc_path, index=False, encoding="utf-8-sig")

        return str(path)
