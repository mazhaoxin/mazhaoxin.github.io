# 养老金测算 By MaZhaoxin @2020-7-10
# 
# 参考:
#  - http://www.shanghai.gov.cn/newshanghai/xxgkfj/hff1770.pdf
#  - http://si.12333.gov.cn/157569.jhtml


def calc_pension(start_work_year, start_work_age, stop_work_age, gender, z, z2, k_avg_salary, k_personal_rate, k_yuebao_rate):
    # 中间参数计算
    if gender.lower()=='m':
        get_money_age = 60  # 可以领取养老金的年龄
        n_personal = 139/12 # 个人账户养老金计发月数/12
    elif gender.lower()=='f':
        get_money_age = 55
        n_personal = 170/12
    else:
        error('Gende只能是M或者F。')
    get_money_year = start_work_year+(get_money_age-start_work_age)

    # 计算

    years = list(range(start_work_year, get_money_year+1))
    ages = list(range(start_work_age, get_money_age+1))
    states = []
    avg_moneys = []
    zs = []
    personal_moneys = []
    company_moneys = []
    personal_moneys_sum = []
    personal_added_moneys = []
    personal_added_moneys_sum = []

    for i in range(len(years)):
        if ages[i]<stop_work_age:
            states.append('在岗\t')
            zs.append(z)
        elif i==len(years)-1:
            states.append('退休\t')
            zs.append(0)
        else:
            states.append('灵活就业')
            zs.append(z2)

        if i==0:
            avg_moneys.append(1)
        else:
            avg_moneys.append(avg_moneys[i-1]*(1+k_avg_salary))

        personal_moneys.append(0.08*zs[i]*avg_moneys[i])
        company_moneys.append(0.16*zs[i]*avg_moneys[i])

        if states[i]=='在岗\t':
            personal_added_moneys.append(0)
        elif states[i]=='灵活就业':
            personal_added_moneys.append(personal_moneys[i]+company_moneys[i])
        else:
            personal_added_moneys.append(0)

        if i==0:
            personal_moneys_sum.append(0)
            personal_added_moneys_sum.append(0)
        else:
            personal_moneys_sum.append(personal_moneys_sum[i-1]*(1+k_personal_rate)+personal_moneys[i])
            personal_added_moneys_sum.append(personal_added_moneys_sum[i-1]*(1+k_yuebao_rate)+personal_added_moneys[i])

    details = list(zip(years, ages, avg_moneys, states, zs, personal_moneys, company_moneys, personal_moneys_sum, personal_added_moneys, personal_added_moneys_sum))

    z_actual = list(filter(lambda z: z!=0, zs))
    n = len(z_actual) # 实际缴费年限
    z_avg = sum(z_actual)/n

    personal_money = personal_moneys_sum[-1]/n_personal
    basic_money = (1+z_avg)/2*n/100*avg_moneys[-1]
    all_money = personal_money+basic_money

    return (details, avg_moneys[-1], personal_moneys_sum[-1], n, all_money, personal_money, basic_money, personal_added_moneys_sum[-1])


def print_details(details):
    print('年份\t年龄\t上年社平工资\t状态\t\t缴费工资指数\t个人缴费\t公司缴费\t个人账户余额\t灵活就业缴费\t灵活就业缴费累计')
    for (year, age, avg_money, state, z, personal_money, company_money, personal_money_sum, personal_added_money, personal_added_money_sum) in details:
        print('%d\t%d\t%.2f\t\t%s\t%.1f\t\t%.2f\t\t%.2f\t\t%.2f\t\t%.2f\t\t%.2f' % (
              year, age, avg_money, state, z, personal_money, company_money, personal_money_sum, personal_added_money, personal_added_money_sum))
    print()


def print_brief(avg_money, personal_money_sum, n, all_money, personal_money, basic_money, personal_added_moneys_sum):
    print('退休时的社平工资：%.2f' % avg_money)
    print('退休时的个人账户余额：%.2f' % personal_money_sum)
    print('实际缴费年限：%d' % n)
    print('退休时的养老金（每年）：%.4f（其中个人账户%.4f，基本养老金%.4f）' % (all_money, personal_money, basic_money))
    print('退休时的养老金（每月）：%.4f（其中个人账户%.4f，基本养老金%.4f）' % (all_money/12, personal_money/12, basic_money/12))
    print('退休时的养老金为社平工资的%.2f倍' % (all_money/avg_money))
    print('灵活就业缴费总额为社平工资的%.2f倍' % (personal_added_moneys_sum/avg_money))
    print('*Note: 以上测算无特别注明的均以年为单位。')
    

if __name__=='__main__':
    # 参数
    start_work_year = 2013  # 开始工作的年份，只用来显示，无关紧要
    start_work_age = 25     # 开始工作的年龄
    stop_work_age = 50      # 干不下去的年龄
    gender = 'm'            # 性别，只能是'm'或'f'，会影响领养老金的年龄
    z = 3.0                 # 缴费工资指数，在0.6~3之间
    z2 = 1.5                # 灵活就业期间的缴费指数，在0或0.6~3之间，0为不再缴费
    k_avg_salary = 0.05     # 社会平均工资的增长速度
    k_personal_rate = 0.02  # 个人账户记账利率
    k_yuebao_rate = 0.02    # 理财利率

    (details, avg_money, personal_money_sum, n, all_money, personal_money, basic_money, personal_added_money_sum) = calc_pension(
        start_work_year, start_work_age, stop_work_age, gender, z, z2, k_avg_salary, k_personal_rate, k_yuebao_rate)
    print_details(details)
    print_brief(avg_money, personal_money_sum, n, all_money, personal_money, basic_money, personal_added_money_sum)
    
