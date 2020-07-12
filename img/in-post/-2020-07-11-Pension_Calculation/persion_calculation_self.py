from persion_calculation import calc_pension


def persion_calculation_self(stop_work_age, gender, z2):
    # 参数
    start_work_year = 2013  # 开始工作的年份，只用来显示，无关紧要
    start_work_age = 25     # 开始工作的年龄
#    stop_work_age = 50      # 干不下去的年龄
#    gender = 'm'            # 性别，只能是'm'或'f'，会影响领养老金的年龄
    z = 3.0                 # 缴费工资指数，在0.6~3之间
#    z2 = 1.5                # 灵活就业期间的缴费指数，在0或0.6~3之间，0为不再缴费
    k_avg_salary = 0.05     # 社会平均工资的增长速度
    k_personal_rate = 0.02  # 个人账户记账利率
    k_yuebao_rate = 0.02    # 理财利率

    (details, avg_money, personal_money_sum, n, all_money, personal_money, basic_money, personal_added_money_sum) = calc_pension(
        start_work_year, start_work_age, stop_work_age, gender, z, z2, k_avg_salary, k_personal_rate, k_yuebao_rate)

    return (all_money/avg_money, personal_added_money_sum/avg_money)


if __name__=='__main__':
    z2s_added = [0, 0.6, 1, 2, 3]
    gender = 'f'

    if gender.lower()=='m':
        get_money_age = 60  # 可以领取养老金的年龄
        stop_work_ages = [40, 45, 50, 55]
    elif gender.lower()=='f':
        get_money_age = 55
        stop_work_ages = [40, 45, 50]
    else:
        error('Gende只能是M或者F。')

    n_added_years = []
    z2s = []
    r_moneys = []
    r_added_moneys = []
    n_payback_years = []

    stop_work_ages.sort(reverse=True)
    for stop_work_age in stop_work_ages:
        for z2 in z2s_added:
            (r_money, r_added_money) = persion_calculation_self(stop_work_age, gender, z2)
            if z2 == 0:
                r_money_noadd = r_money
                n_payback_year = 0
            else:
                n_payback_year = r_added_money/(r_money-r_money_noadd)

            n_added_years.append(get_money_age-stop_work_age)
            z2s.append(z2)
            r_moneys.append(r_money)
            r_added_moneys.append(r_added_money)
            n_payback_years.append(n_payback_year)

    print('灵活就业年数\t缴费工资指数\t归一化养老金\t归一化自费总额\t费用比养老金变化量')
    for (n_added_year, z2, r_money, r_added_money, n_payback_year) in zip(n_added_years, z2s, r_moneys, r_added_moneys, n_payback_years):
        print('%d\t\t%.1f\t\t%.2f\t\t%.2f\t\t%.2f' % (n_added_year, z2, r_money, r_added_money, n_payback_year))
        
