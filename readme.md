<img title="" src="./ico.jpeg" alt="" width="357" data-align="center">

## 七星指令计算器

版本:Version 0.001 测试版本 

    

> 支持平台

![windows](https://img.shields.io/badge/%E6%94%AF%E6%8C%81%E5%B9%B3%E5%8F%B0-Windwos-blue)

![Static Badge](https://img.shields.io/badge/%E6%94%AF%E6%8C%81%E5%B9%B3%E5%8F%B0-Linux-red)

> 项目简介

Linux平台终端,指令计算器 . 通过执行 打包的二进制程序运行程序(打包 main.py). 可以将程序添加到Linux环境变量中. 通过快捷指令调用.

> 七星指令计算器语言 

计算器支持的运算仅限于整数,后续更新其他类型变量的运算 . 暂时不支持负数输入,如需调用 请使用 零减去整数.以下是语法简要,可以嵌套使用.

- 变量

```c
variable = Value
```

- 加减乘除运算

```c
Value * Value
```

```c
Value + Value
```

```c
Value - Value
```

```c
Value / Value
```

- 逻辑预算

```c
a & b //与运算
```

```c
a | b // 或运算
```

- 关系运算

```c
a > b 
```

```c
a >= b 
```

```c
a < b
```

```c
a <= b
```

- 优先级运算

```
(a+b) * c
```
