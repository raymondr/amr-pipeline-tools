import matplotlib.pyplot as plt

y = [0.9980713597,
0.9980713597,
0.9929283189,
0.9803921569,
0.9463195114,
0.9103182257,
0.8691738991,
0.7978142077,
0.7984570878]
y1 = [0.8161362906]
y2= [0.6788813886]

x = [1,
0.05895953757,
0.04624277457,
0.03699421965,
0.03352601156,
0.0161849711,
0.003468208092,
0.0,
0.0]

x1=[0.1387283237]
x2=[0.002312138728]

plt.plot(x,y)
plt.plot(x[-3:-2], y[-3:-2],'bx')
plt.plot(x1, y1,'ro')
plt.plot(x2, y2, 'go')
plt.legend(['NIFA', 'NIFA Optimized', 'Resfams Full', 'Resfams'])
plt.xlabel('False positive rate from gingivalis genome'); plt.ylabel('True positive rate from simulated reads');
#plt.title('ROC with various HMM cut off thresholds for NIFA compared with Resfams')
plt.axis([-.005, 1, 0, 1])
plt.show()
