from django.db import models

# Create your models here.
# 图书管理系统，书 作者  出版社


# 出版社
class Publisher(models.Model):
    id = models.AutoField(primary_key=True)  # 自增的ID主键
    # 创建一个varchar(64)的唯一的不为空的字段
    name = models.CharField(max_length=64, null=False, unique=True)
    addr = models.CharField(max_length=64, null=False)

    def __str__(self):
        return "<Publisher Object:{}>".format(self.name)


# 书
class Book(models.Model):
    #  自增的ID主键
    id = models.AutoField(primary_key=True)
    # null 数据库表中的字段是否可以为空
    # unique 是否唯一
    title = models.CharField(max_length=64, null=False, unique=True)
    # 关联出版社
    # publisher在ORM中是一个出版社对象，但是在数据库是以出版社id存储
    publisher = models.ForeignKey(to="Publisher")

    def __str__(self):
        return "<Book Object:{}>".format(self.title)


# 作者
class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, null=False, unique=True)
    # 告诉ORM Author这张表和Book表是多对多的关联关系，ORM自动生成第三张表
    book = models.ManyToManyField(to="Book")

    def __str__(self):
        return "<Author Object:{}>".format(self.name)