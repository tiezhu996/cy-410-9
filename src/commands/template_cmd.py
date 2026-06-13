import click

from src.core.template import TemplateGenerator


@click.command(help="下载标准导入模板，包含示例数据和字段说明")
@click.option("--output", required=True, type=click.Path(), help="输出文件路径")
@click.option("--format", "output_format", type=click.Choice(["csv", "excel"]), default="csv", show_default=True, help="文件格式")
@click.option("--sample/--no-sample", default=True, show_default=True, help="是否包含示例数据")
def template(output: str, output_format: str, sample: bool) -> None:
    path = TemplateGenerator().generate(output_format, output, with_sample=sample)
    click.echo(f"模板已生成：{path}")
    if output_format == "csv":
        import os
        from pathlib import Path
        desc_path = Path(output).with_name(f"{Path(output).stem}_字段说明.csv")
        if desc_path.exists():
            click.echo(f"字段说明：{desc_path}")
    click.echo("请按模板填写数据后使用 import 命令导入")
