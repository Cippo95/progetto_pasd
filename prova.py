import matplotlib.pyplot as plt

left_coordinates=[1,2,3,4,5]
heights=[10,20,30,15,40]
bar_labels=['One','Two','Three','Four','Five']
plt.bar(left_coordinates,heights,tick_label=bar_labels,width=0.6,color=['red','black'])
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title("A simple bar graph")
#plt.show()
plt.savefig("prova")