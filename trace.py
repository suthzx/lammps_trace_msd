import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
def slopeline1(x,y):
#     best_fit_line = np.poly1d(np.polyfit(y, x, 1))(y)
#     slope = (y[-1] - y[0]) / (x[-1] - x[0])
#     angle = np.arctan(slope)
#     reg = linear_model.LinearRegression()
#     reg.fit (np.array(range(len(x))).reshape(-1,1),np.array(y).reshape(-1,1))
    return linregress(x,y)[0]


def main(path3,tracepath):
    splitcomcept=[]
    rx=[i*0.0 for i in range(15000)]
    ry=[i*0.0 for i in range(15000)]
    rz=[i*0.0 for i in range(15000)]
    flag=0
    number=1
    msd=0.0
    MSD=[]
    slopelist=[]
    y=[]
    step=0.001    #步长
    pathtrace=os.path.join(path3,'MSD.txt')
    tracemsd=open(pathtrace,'w+')
    with open(tracepath,"r") as file:
        for line in file:
            if len(line[1:15].split())>1:
                if (line[1:15].split())[1]=='TIMESTEP':
                    flag=0
                    msd=msd/number
                    tracemsd.write(str(msd)+'\n')
                    MSD.append(msd)
#               print(flag)
                    msd=0.0
                    number=0
            if flag==1:
                splitcomcept=line.split()
#                 vx.append(splitcomcept[2])
#                 vy.append(splitcomcept[3])
#                 vz.append(splitcomcept[4])
                rx[tick]+=float(splitcomcept[2])*step
                ry[tick]+=float(splitcomcept[3])*step
                rz[tick]+=float(splitcomcept[4])*step
                xx=rx[tick]**2+ry[tick]**2+rz[tick]**2
                number+=1
                msd+=xx
                tick=tick+1
#                 print(splitcomcept[2],'  ',splitcomcept[3],'  ',splitcomcept[4])
            if line[1:15]=='TEM: ATOMS id ':
                flag=1
                tick=0
#画MSD曲线及斜率计算
    plt.figure()
    plt.subplot(2,1,1)
    x=[step*j for j in range(len(MSD))]
    fig1=plt.plot(x[1:],MSD[1:])
    for i in range(len(MSD)-8):
        y1=MSD[i:i+2]
#         print(y1)
        x1=[step*j for j in range(2)]
#         print(x1)
        slope1=slopeline1(x1,y1)
        slopelist.append(slope1)
    plt.subplot(2,1,2)    
    fig2=plt.plot(x[1:len(slopelist)],slopelist[1:])
    plt.savefig("./test.png",dpi=600)
    plt.show()
    tracemsd.close()
    pathslope=os.path.join(path3,'slopture.txt')
    slope=open(pathslope,'w')
    for i in slopelist[1:]:
        slope.write(str(i)+'\n')
    slope.close()

path=r"/public/home/yangwen/suth_work/lamm/feni"   #输入到相路径
if __name__ == '__main__':
    for i in os.listdir(path):
        path1=os.path.join(path,i)
        for j in os.listdir(path1):
            if j[-1:]=='V':
                path2=os.path.join(path1,j)
                for k in os.listdir(path2):
                    if k[-3:]=="10K":
                        path3=os.path.join(path2,k)
                        for m in os.listdir(path3):
                            if m[-8:]=="ammpstrj":
                                tracepath=os.path.join(path3,m)
                                main(path3,tracepath)