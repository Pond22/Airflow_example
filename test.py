'''
เขียวต้องการออมเงิน วันละ 5 บาท
วันแรกของปีคือวันจันทร์
ปีนั้นมี 366 วัน
ทุกวันศุกร์ จะออมเงิน 8 บาท
ทุกวันที่ 1 และ 16 ของเดือนจะออมเงิน 10 บาท
ทุก 3 เดือนจะออมเงิน 100 บาท
ปีนั้นทั้งปี เขียวจะมีเงินออมเท่าไหร่
จงเขีบนเป็นโปรแกรมภาษา java แสดงยอดสรุปทุกเดือน ว่าแต่ละเดือนได้เท่าไหร่ และสรุปยอดรวมสะสมด้วย  โจทย์กำกวมไม่แน่ใจว่าเงินที่เพิ่มมา เช่น วันที่ 1 หรือ 16 ของทุกเดือนจะยังออม 5 บาทแต่ออมเพิ่ทอีก 10 บาทไหม
'''

mon ='mon'
tue ='tue'
wed='wed'
thu ='thu'
fri='fri'
sat='sat'
sun='sun'

day =['mon', 'tue', 'wed', 'thu', 'fri', 'sat','sun']

year = 366

kom = 31
yon =30

month =['kom','spi','kom','yon','kom','yon','kom','kom','yon','kom','yon','kom']
daymonth = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31] 

money =0
total_money = 0
tem_day =0
for i in range(len(daymonth)):
    tem_month = i+1
    day_count = daymonth[i]
    """ print(f'เดือนที่ {tem_month} มีทั้งหมด {daymonth[i]} วัน') """
    
    if tem_month % 3 ==0 :
        """ print(f'เดือนที่ {tem_month} == 3') """
        money+=100
    
    for j in range(day_count):
        if tem_day > 7:
            tem_day=1
        
        if j == 1 or j == 16: #ให้ความสำคัญการออมที่มากที่สุดก่อนเพราะไม่รู่ว่าโจทย์ต้องการอะไร
            money+=10
        elif tem_day == 5:
            money+=8
        else:
            money+= 5
        
        """ if j == 1 or j == 16:
            money+=10 """
            
        tem_day+=1
    total_money += money
    print(f'เดือนที่ {tem_month} มีเงินออมทั้งหมด {money} บาท')
    money =0
    
print(f'ทั้งปีมีเงินออมทั้งหมด {total_money} บาท')
    


