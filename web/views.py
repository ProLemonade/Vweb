from django.shortcuts import render, redirect


from web.models import CodeFile
from web.models import DataType, DataValue, DataItem
from web.models import ProcessExplanation, ProcessFormula, ProcessVariable

from django.core.management.base import BaseCommand
from django.db.models import Prefetch
from django.http import JsonResponse
from django.conf import settings
from pathlib import Path
import subprocess
import tempfile
import base64
import json
import os
import re

# Create your views here.

def origin(request):
    return render(request, 'Origin.html')

def core(request):
    return render(request, 'CORE.html')

def data(request):
    data_types = DataType.objects.all()
    data_items = DataItem.objects.all()
    data_values = DataValue.objects.all()
    return render(request, 'DATA.html', {
        'data_types': data_types,
        'data_items': data_items,
        'data_values': data_values,
        })

def code(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        # 在线编程功能
        if action == 'run_code':
            code = request.POST.get('code')
            language = request.POST.get('language')
            with tempfile.NamedTemporaryFile(mode='w', suffix=f'.{language}', delete=False) as temp_file:
                temp_file.write(code)
                temp_file_path = temp_file.name
            try:
                img_path = os.path.join(settings.MEDIA_ROOT, 'output.png')

                if language == 'python':
                    python_code = f"""
# -*- coding: utf-8 -*-
{code}
plt.savefig("{img_path}")
plt.close()
"""
                    with open(temp_file_path, 'w') as f:
                        f.write(python_code)
                    result = subprocess.run(['python', temp_file_path], capture_output=True, text=True, timeout=30)
                elif language == 'julia':
                    julia_code = f"""
{code}
savefig("{img_path}")
"""
                    with open(temp_file_path, 'w') as f:
                        f.write(julia_code)
                    result = subprocess.run(['julia', temp_file_path], capture_output=True, text=True, timeout=30)
                elif language == 'matlab':
                    matlab_code = f"""
{code}
saveas(gcf, '{img_path}');
close all;
"""
                    with open(temp_file_path, 'w') as f:
                        f.write(matlab_code)
                    result = subprocess.run(
                        ['matlab', '-nodisplay', '-nosplash', '-nodesktop', '-r', f"run('{temp_file_path}');exit;"],
                        capture_output=True, text=True, timeout=30
                    )

                if os.path.exists(img_path):
                    with open(img_path, 'rb') as img_file:
                        img_data = base64.b64encode(img_file.read()).decode('utf-8')
                    os.remove(img_path)
                    return JsonResponse(
                        {'image': img_data, 'output': result.stdout if result.returncode == 0 else result.stderr})
                else:
                    return JsonResponse({'output': result.stdout if result.returncode == 0 else result.stderr})
            except subprocess.TimeoutExpired:
                return JsonResponse({'error': 'Code execution timed out'})
            finally:
                os.unlink(temp_file_path)  # 清理缓存

    # 用list是为了把内容先全部加载好 便于后续直接取等 不用反复深入数据库
    files = list(CodeFile.objects.values('name', 'language', 'content_tags', 'content_code'))
    # 没用list就没有全部加载 取等找到目标数据后 也得老老实实加载对应内容
    processes = ProcessExplanation.objects.all()

    # 读取一些乱七八糟的代码段落凑数
    file_path = Path(settings.BASE_DIR) / 'web' / 'static' / 'txt' / 'code-simu.txt'
    simu_sections = parse_code_file(file_path)

    file_path = Path(settings.BASE_DIR) / 'web' / 'static' / 'txt' / 'code-tools.txt'
    tool_sections = parse_code_file(file_path)

    return render(request, 'CODE.html', {
        'files': files,
        'processes': processes,
        'simu_sections': simu_sections,
        'tool_sections': tool_sections
    })
def parse_code_file(file_path: Path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    simu_sections = []
    raw_sections = content.split('###')[1:]
    for raw_section in raw_sections:
        section = {'phases': []}
        lines = [line.strip() for line in raw_section.split('\n') if line.strip()]
        if lines:
            section['section_name'] = lines[0]
            lines = lines[1:]
        current_tip = None
        current_code = []
        for line in lines:
            if line.startswith('#'):
                if current_tip is not None:
                    section['phases'].append({
                        'tip': current_tip,
                        'code': '\n'.join(current_code).strip()
                    })
                    current_code = []
                current_tip = line[1:].strip()
            else:
                current_code.append(line)
        if current_tip is not None:
            section['phases'].append({
                'tip': current_tip,
                'code': '\n'.join(current_code).strip()
            })
        simu_sections.append(section)
    return simu_sections


def visual(request):
    data_items = DataItem.objects.all().values_list('name', flat=True)
    return render(request, 'visual.html', {
        'conditions': list(data_items),
    })

def report(request):
    image_dir = Path(settings.BASE_DIR) / 'web' / 'static' / 'plots'

    image_files = []
    for filename in os.listdir(image_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            image_url = 'plots/' + filename

            image_files.append({
                'url': image_url,
                'name': filename,
            })
    return render(request, 'report.html', {'images': image_files})


def test_catalog(request):
    return render(request, 'test_catalog.html')
def test_code_simu_refresh(request):
    if request.method == 'POST':
        ProcessExplanation.objects.all().delete()

        md_file = Path(settings.BASE_DIR) / 'web' / 'static' / 'txt' / 'processes.md'

        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 以一级标题为界 分割出多条processes
        processes = re.split(r'^#\s+', content, flags=re.MULTILINE)
        processes = [p for p in processes if p.strip()]
        # 对每一条process进行处理
        for proc in processes:
            lines = proc.strip().splitlines()
            process_name = lines[0].strip()

            code_match = re.search(r'##\s*Process Code\s*```(?:\w+)?(.*?)```', proc, re.DOTALL)
            process_code = code_match.group(1).strip() if code_match else ""

            app_match = re.search(r'##\s*Process Application\s*(.*?)(?=##\s*ProcessFormula|\Z)', proc, re.DOTALL)
            process_application = app_match.group(1).strip() if app_match else ""

            proc_explain, _ = ProcessExplanation.objects.update_or_create(
                name=process_name,
                defaults={
                    'process_code': process_code,
                    'process_application': process_application
                }
            )

            # 公式可能有多个
            proc_explain.formulas.all().delete()
            formula_section_match = re.search(r'##\s*ProcessFormula\s*(.*)', proc, re.DOTALL)
            if formula_section_match:
                formula_section = formula_section_match.group(1)
                # 以一级标题为界 分割出多条formula_blocks
                formula_blocks = re.split(r'^###\s+', formula_section, flags=re.MULTILINE)
                # 对每一条process进行处理
                for fblock in formula_blocks[1:]:
                    fblock_lines = fblock.strip().splitlines()
                    if not fblock_lines:
                        continue
                    formula_text = fblock_lines[0].strip()
                    formula_obj = ProcessFormula.objects.create(
                        process_explanation=proc_explain,
                        formula_text=formula_text
                    )
                    for line in fblock_lines[1:]:
                        line = line.strip()
                        if not line:
                            continue
                        # 每行一个变量 以--为界 分割出具体介绍
                        parts = re.split(r'\s*--\s*', line)
                        if len(parts) >= 4:
                            variable_name = parts[0].strip()
                            variable_unit = parts[1].strip()
                            variable_mean_en = parts[2].strip()
                            variable_mean_zh = parts[3].strip()
                            ProcessVariable.objects.create(
                                process_formula=formula_obj,
                                variable_name=variable_name,
                                variable_unit=variable_unit,
                                variable_mean_en=variable_mean_en,
                                variable_mean_zh=variable_mean_zh
                            )
        return redirect('/test/codes')

    process_explanations = ProcessExplanation.objects.all()
    return render(request, 'test_codes.html', {
        'process_explanations': process_explanations
    })
def test_code_visu_refresh(request):
    if request.method == 'POST':
        CodeFile.objects.all().delete()  # 清空数据后重新加载
        code_dir = Path(settings.BASE_DIR) / 'web' / 'static' / 'codes'
        lang_map = {'.py': 'python', '.jl': 'julia', '.m': 'matlab'}

        for file in code_dir.glob('*.*'):
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                lines = content.split('\n', 1)  # 代码首行放的是tag
            CodeFile.objects.create(
                name=file.stem,
                content_tags=lines[0] if lines else "",
                content_code=lines[1] if len(lines) > 1 else "",
                language=lang_map[file.suffix.lower()]
            )
        return redirect('/test/codev')

    files = list(CodeFile.objects.values('name', 'language', 'content_tags', 'content_code'))
    return render(request, 'test_codev.html', {'files': files})
def test_data_list_refresh(request):
    if request.method == 'POST':
        DataType.objects.all().delete()
        DataValue.objects.all().delete()
        DataItem.objects.all().delete()

        type_file = Path(settings.BASE_DIR) / 'web' / 'static' / 'txt' / 'data-types.txt'
        item_file = Path(settings.BASE_DIR) / 'web' / 'static' / 'txt' / 'data-items.txt'

        with open(type_file, 'r', encoding='utf-8') as f:
            current_type = None  # 预设父类
            for line in f:
                line = line.strip()
                if not line:
                    continue  # 遍历非空白的每行
                if line.startswith('>'):
                    if current_type:  # 目前父类
                        DataValue.objects.get_or_create(
                            type=current_type,
                            value=line[1:].strip()  # 去掉 >
                        )
                else:
                    current_type, _ = DataType.objects.get_or_create(name=line)  # 父类

        with open(item_file, 'r', encoding='utf-8') as f:
            current_item = None
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if not line.startswith('>'):
                    current_item, _ = DataItem.objects.get_or_create(name=line)
                    continue

                tag_line = line[1:].strip()
                for tag in tag_line.split(';'):
                    tag = tag.strip()
                    if not tag:
                        continue

                    type_name, value = tag.split('-', 1)
                    type_name = type_name.strip()
                    value = value.strip()

                    dtype = DataType.objects.get(name=type_name)
                    #print(type_name)
                    dvalue = DataValue.objects.get(type=dtype, value=value)

                    current_item.tags.add(dvalue)

    data_types = DataType.objects.all()
    data_items = DataItem.objects.all()
    data_values = DataValue.objects.all()
    return render(request, 'test_data.html', {
        'data_types': data_types,
        'data_items': data_items,
        'data_values': data_values,
    })
