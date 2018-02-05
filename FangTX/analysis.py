# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt

class analysis(object):

    # 统计各地段区域的占比
    # 以饼图展现
    # series:pandas的series元素，即列对象
    # 返回 img对象：生成的图片（location_percent.jpg）
    # 返回 series对象
    # 格式为元组(series, img)
    def show_pie(self, series, flag=0, img_name=''):
        # 统计各元素出现的次数,返回一个Series对象
        result_location = series.value_counts()
        x_than_flag = result_location[result_location >= flag]  # 选取数值大于等于20的，返回Series
        x_little_flag = result_location[result_location < flag]  # 选取数值小于20的，返回Series
        x_other = pd.Series({'其他': x_little_flag.sum()})  # 创建一个Series，表示数值少于20的所有之和
        x_new = x_than_flag.append(x_other)  # 将x_other Series加到x_than_20之后，形成新的Series
        # 设置字体
        plt.rcParams['font.sans-serif'] = ['SimHei']
        # 解决保存图像是负号'-'显示为方块的问题
        plt.rcParams['axes.unicode_minus'] = False
        # 对结果进行可视化处理
        # 指定图像大小
        img = plt.figure(figsize=(12, 5.5))
        img.suptitle(img_name + " 统计情况", fontsize=15)
        # 子图：即在一张图片中显示多个子图
        # subplot(numRows, numCols, plotNum)
        # 图表的整个绘图区域被分成numRows行和numCols列，plotNum参数指定创建的Axes对象所在的区域，如何理解呢？
        # 如果numRows ＝ 3，numCols ＝ 2，那整个绘制图表样式为3X2的图片区域，用坐标表示为（1，1），（1，2），（1，3），（2，1），（2，2），（2，3）。
        # 这时，当plotNum ＝ 1时，表示的坐标为（1，3），即第一行第一列的子图；
        # 放在子图的第一个位置：第1行第1列
        ax1 = plt.subplot(1, 2, 1)
        explode = [0] * len(x_new)  # 生成一个列表,长度（元素个数）为len(x_new)，其元素全为数值0
        explode[0] = 0.05  # 将第一个元素改为0.5

        # 将x_new用“饼图”展示
        ax1.pie(
            x=x_new,  # 指定绘图的数据
            labels=x_new.index,  # (每一块)饼图外侧显示的说明文字
            autopct='%1.1f%%',  # 控制饼图内百分比设置
            pctdistance=0.8,  # 指定autopct的位置刻度
            startangle=0,  # 指定起始角度
            labeldistance=1.03,  # 指定label的位置刻度
            explode=explode  # (每一块)离开中心距离,必须是列表，长度与x长度要一致
        )
        ax1.set_title('数量不低于 %d 的区域' %flag)  # 指定图片标题
        # 放在子图的第二个位置：：第1行第2列
        ax2 = plt.subplot(1, 2, 2)
        # 将x_little_20用“饼图”展示
        ax2.pie(
            x=x_little_flag,
            labels=x_little_flag.index,
            autopct='%1.1f%%',
            pctdistance=0.8,
            startangle=90,
            labeldistance=1.03,
            radius=0.8  # 控制饼图半径
        )
        ax2.set_title('数量低于 %d 的区域(其他)' %flag)  # 指定图片标题
        # legend : 显示图示labeldistance
        # plt.legend()
        # 显示出我们创建的所有绘图对象。
        plt.show()
        # 保存图片
        #img.savefig('location_percent.jpg')

        return (series, img)


    # 统计每一个区域中，在售的小区信息
    # dataframe pandas dataframe对象
    # name 小区名称
    def show_name_percent(self, dataframe, name=''):
        # 通过name的值，在dataframe中找到其所在的行号
        low_index_list = dataframe[dataframe.location == name].index.tolist()
        # 通过行号，找到小区名称
        # 从'name列取值，行号为low_index_list。存放到列表
        low_name = []
        for i in low_index_list:
            a = dataframe['name'][i]
            low_name.append(a)
        # 存放为series对象
        name_series = pd.Series(low_name, index=low_index_list)
        # 调用数据分析方法-饼图显示
        series, img = self.show_pie(name_series,4,name)
        pass


    # 数据清洗过程
    # 返回DataFrame对象
    # location: 指定区域
    # name:指定小区名称
    # flag: 总价阀值，清除比该值大的数据
    def wash_data(self, dataframe, location='', name='', flag=10000):
        # 选取列名为location，返回DataFrame对象
        df_location = dataframe[dataframe.location == location]
        # 选取行名为name，返回DataFrame对象
        df_name = df_location[df_location.name ==name]
        # 数据清洗：去除总价大于flag的数据
        df_name = df_name[df_name.total_price <= flag]
        # 将清洗后的房源数据返回
        return df_name



    # 绘制详细信息
    # DataFrame 为清洗之后的数据对象
    def show_info(self, DataFrame):
        # 取得area数据列表
        area_list = DataFrame['area'].values
        # 取得总价数据列表
        total_price_list = DataFrame['total_price'].values
        # 取得单价数据列表
        price_list = DataFrame['price'].values
        # 创制一个图形对象
        fig = plt.figure(figsize=(12, 6), dpi=120)
        # 设置字体
        plt.rcParams['font.sans-serif'] = ['SimHei']
        # 解决保存图像是负号'-'显示为方块的问题
        plt.rcParams['axes.unicode_minus'] = False
        # 增加总价格-面积 图表
        total_price_area_ax = fig.add_subplot(2,1,1)
        # 在价格图表中右边增加面积y坐标
        area_ax = total_price_area_ax.twinx()
        # 左边y轴标签
        total_price_area_ax.set_ylabel('总价格 / 万元', color='b')
        # 右边y轴标签
        area_ax.set_ylabel('面积 / 平方米', color='r')
        # x轴标签
        a = DataFrame['name'].values[0]
        b = DataFrame['location'].values[0]
        # 图形名称
        fig.suptitle('[' + b + ' - ' +  a +'] 小区价格图', fontsize=15)
        # 绘制总价格线plot
        total_price_area_ax.plot(total_price_list, '-o', ms=5, lw=2,  mfc='orange', label = "总价格")
        # 绘制面积线plot
        area_ax.plot(area_list, '--*',color='r', alpha=0.8, label = "面积")
        # 显示标签
        total_price_area_ax.legend(loc=2)
        area_ax.legend(loc=1)
        # 显示网格
        total_price_area_ax.grid(color='b', alpha=0.3, linestyle="-")
        area_ax.grid(color='r', alpha=0.3,linestyle="-.")

        # 增加单价图表
        price_ax = fig.add_subplot(2, 1, 2)
        # 设置x轴标签
        price_ax.set_ylabel('单价 元/平方米', color='orange')
        # 绘制单价线plot
        price_ax.plot(price_list, '-', mfc='orange', label = "单价", color='orange')
        # 显示网格
        price_ax.grid(color='orange',alpha=0.3, linestyle="-.")
        # 显示数值标签
        for x,y in zip(price_list,range(len(price_list))):
            price_ax.text(y, x, x, bbox=dict(facecolor='white', alpha=0.5), ha='left', va= 'bottom',fontsize=7)

        # 绘制平均单价线
        # 均值
        value = sum(price_list) / len(price_list)
        # 增加均值线
        price_ax.plot([value]*(len(price_list)), '--', label = "均价", color='g',lw=1)
        # 显示标签
        price_ax.legend(loc=3)










        fig.show()


        pass







if __name__ == '__main__':
    path = 'data.csv'
    path2 = 'data_analysis.xlsx'
    # 读入文件
    # df：任意的Pandas DataFrame对象
    # s：任意的Pandas Series对象
    df = pd.read_csv(path)
    a = analysis()
    a.show_pie(df['location'], 10)
    a.show_name_percent(df, '增城 新塘南')
    a.show_info(a.wash_data(df,location='增城 新塘南', name='金地香山湖', flag=300))