#!/usr/bin/env python
# coding: utf-8

# In[1]:



class Node:
    def __init__(self,event=None,value=None):
        self.event=event
        self.value=value
        self.left_child=None
        self.right_child=None



class binarySearchTree:
    
    def __init__(self):
        self.root=None
    
    
    def insert(self, event, value):
        if self.root==None:
            self.root=Node(event,value)
        else:
            self.recursive_insert(self.root,event,value)       
    def recursive_insert(self,node,event,value):
        if value<node.value:
            if node.left_child==None:
                node.left_child=Node(event,value)
            else:
                self.recursive_insert(node.left_child,event,value)
        else:
            if node.right_child==None:
                node.right_child=Node(event,value)
            else:
                self.recursive_insert(node.right_child,event,value)

                
    def print_tree(self):
        if self.root!=None:
            self.rec_print_tree(self.root)
    def rec_print_tree(self,node):
        if node!=None:
            self.rec_print_tree(node.left_child)
            print(node.event,node.value)
            self.rec_print_tree(node.right_child)
    
    def special_print_tree(self):
        if self.root!=None:
            self.rec_special_print_tree(self.root)
    def rec_special_print_tree(self,node):
        if node!=None:
            self.rec_special_print_tree(node.left_child)
            print(node.event.person, " becomes ", node.event.state, " at time ", node.value)
            self.rec_special_print_tree(node.right_child)
            
            
            
    
    def height(self):
        if self.root!=None:
            return self.rec_height(self.root,0)
        else:
            return 0
    def rec_height(self,node,height):
        if node==None:
            return height
        else:
            l_height=self.rec_height(node.left_child,height+1)
            r_height=self.rec_height(node.right_child,height+1)
            return max(l_height,r_height)
    
    
    def search(self,value): #might mess up with floats
        if self.root!=None:
            return self.rec_search(self.root,value)
        else:
            return False
    def rec_search(self,node,value):
        print(value-node.value)
        if value==node.value:
            return True
        elif value<node.value and node.left_child!=None:
            return self.rec_search(node.left_child,value)
        elif value>node.value and node.right_child!=None:
            return self.rec_search(node.right_child,value)
        return False
        
    def smallest(self):
        if self.root==None:
            return False
        return self.rec_smallest(self.root)
    def rec_smallest(self,node):
        if node.left_child==None:
            return node
        return self.rec_smallest(node.left_child)
        
    def next_event(self, time): #assumes no two events at same time
        if self.root==None:
            return False
        return self.rec_next_event(self.root,time)
    def rec_next_event(self,node,time):
        if time<node.value:
            if node.left_child==None:
                return node
            elif time<node.left_child.value:
                return self.rec_next_event(node.left_child,time)
            return node
        else:
            if node.right_child!=None:
                return self.rec_next_event(node.right_child,time)
            return False
    
    def remove_smallest(self):
        if self.root==None:
            return False
        return self.rec_remove_smallest(self.root,None)
    def rec_remove_smallest(self,node,prev_node):
        if node.left_child==None:
            if prev_node==None:
                x=self.root
                self.root=node.right_child #could be None
                return x
            elif node.right_child!=None:
                prev_node.left_child=node.right_child
            else:
                prev_node.left_child=None
            return node
        return self.rec_remove_smallest(node.left_child,node)
    
    def clear(self):
        self.root = None

