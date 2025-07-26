from django.db import models

# Create your models here.

# Data-Info 数据名称及信息
class DataType(models.Model):
    name = models.CharField(max_length=50, unique=True)  # 不能重复

    def __str__(self):
        return self.name

class DataValue(models.Model):
    type = models.ForeignKey(  # DataValue属于某DataType
        DataType,  # 下属上的一对多关系
        on_delete=models.CASCADE,  # 随所属delete
        related_name='values'  # 可由所属查询
    )
    value = models.CharField(max_length=50)

    class Meta:
        unique_together = [['type', 'value']]  # 不能重复

    def __str__(self):
        return f"{self.type.name} - {self.value}"

class DataItem(models.Model):
    name = models.CharField(max_length=100, unique=True)  # 不能重复 item名称唯一
    tags = models.ManyToManyField(DataValue)  # 可以重复 不同item的标签名称不唯一

    def __str__(self):
        return self.name


# Code-Simulation 模拟代码分段解释
class ProcessExplanation(models.Model):
    name = models.CharField(max_length=100, unique=True)
    process_code = models.TextField()
    process_application = models.TextField()

    def __str__(self):
        return self.name

class ProcessFormula(models.Model):
    process_explanation = models.ForeignKey(
        ProcessExplanation,
        on_delete=models.CASCADE,
        related_name='formulas'
    )
    formula_text = models.TextField()

    def __str__(self):
        return f"{self.formula_text}"

class ProcessVariable(models.Model):
    process_formula = models.ForeignKey(
        ProcessFormula,
        on_delete=models.CASCADE,
        related_name='variables'
    )
    variable_name = models.CharField(max_length=100)
    variable_unit = models.CharField(max_length=50)
    variable_mean_en = models.CharField(max_length=50)
    variable_mean_zh = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.variable_name} ({self.variable_unit})"


# Code-Visualization 绘图代码汇总
class CodeFile(models.Model):
    name = models.CharField(max_length=255)
    content_tags = models.TextField(blank=True)
    content_code = models.TextField()
    language = models.CharField(max_length=50)

    def __str__(self):
        return self.name