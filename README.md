# shuting-yard
Implement shutting_yard algorithm using python

token -> AST

[] -> 递归 -> tree

文法： 语言的规则 

BNF 巴克斯范式 可以通过工具生成解析代码

上下文无关文法 这里不是标准的BNF写法

解释器


解释器执行的过程， 就是通过ast node中不同节点的属性， 进行不同的操作

## 05变量

var a = 1

keyword = var
变量名 = a
赋值操作符 = 

1. 修改语法规则
添加tokens
添加ast node
修改词法解析器规则
修改语法解析器规则
修改解释器

怎么给变量赋值
怎么获取变量的值

符号表 symbol table (dict)

a => 1

function -> 作用域的概念
变量， 就需要判断作用域

func a， func b, 全局变量也要又一个符号表
单独的方法， 也要有单独的符号表