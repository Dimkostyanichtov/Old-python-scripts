#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 12:01:28 2019

@author: gamma-dna
"""

#def convert(s, numRows):
#   if numRows == 1:
#        return s 
#    n = len(s)
#    cycle = 2*numRows - 2
#    strlist = []
#    for i in range(numRows):
#        for j in range(i, n, cycle):
#            strlist.append(s[j])
#            if i != numRows-1 and i != 0 and j+cycle-2*i < n:
#                strlist.append(s[j+cycle-2*i])             
#    newstr = ''.join(strlist)
#    return newstr
                    
            
#s = 'PAYPALISHIRING'
#numRows = 5  
#a = convert(s, numRows)
#print(a)

def maxArea(height):
    
    square = []
    
    for i in xrange(len(height)):
        for j in xrange(i + 1, len(height)):
            square.append((j-i)*min(height[i], height[j]))
        
    return max(square)
                            
a = [1,8,6,2,5,4,8,3,7]
res = maxArea(a)
print(res)