from django.db import models

# Create your models here.

from django.db import models

# Create your models here.
class Areas(models.Model):
    """
    行政区划
    """
    name = models.CharField(max_length=20, verbose_name='名称')
    # self 指明外键是自己这个模型类
    # 使用场景,构建多级关系
    # related_name
    # 一模型对象查询多模型对象 默认 book.heroinfo_set.all()
    # related_name=heros   book.heros.all()
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='subs', null=True, blank=True, verbose_name='上级行政区划')

    class Meta:
        db_table = 'tb_areas'
        verbose_name = '行政区划'
        verbose_name_plural = '行政区划'

    def __str__(self):
        return self.name
