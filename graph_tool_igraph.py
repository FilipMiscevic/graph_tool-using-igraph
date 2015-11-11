import collections
from igraph import *

class Graph(Graph):
    '''A class which extends the attributes of igraph's Graph so that it can be referenced as a graph_tool Graph class.'''
    
    class PropertiesDictWrapper(collections.MutableMapping):
        """A dictionary that stores a PropertiesDict object while updating the underlying Graph attributes."""
    
        def __init__(self, *args, **kwargs):
            self.store = dict()
            self._graph = kwargs.get('_graph')
            self._type = kwargs.get('_type')
            
        def __repr__(self):
            if self._type == 'vs':
                return str(self._graph.vs.attributes())
            elif self._type == 'es':
                return str(self._graph.es.attributes())
            elif self._type == 'g':
                return str(self._graph.attributes())    
            
        def __getitem__(self, key):
            return self.store[key]
                
        def __setitem__(self, key, value):            
            if type(value) == Graph.PropertiesDict:
                value._attr = key
                self.store[key] = value
            #if type(value) == list & len(value) == self.__len__():
                #pass
            if self._type == 'vs':
                self._graph.vs[key] = None#value
            elif self._type == 'es':
                self._graph.es[key] = None#value
            elif self._type == 'g':
                self._graph[key] = value
    
        def __iter__(self):
            if self._type == 'vs':
                return iter(self._graph.vs.attributes())
            elif self._type == 'es':
                return iter(self._graph.es.attributes())
            elif self._type == 'g':
                return iter(self._graph.attributes())
            
        def __len__(self):
            if self._type == 'vs':
                return len(self._graph.vs.attributes())
            elif self._type == 'es':
                return len(self._graph.es.attributes())
            elif self._type == 'g':
                return len(self._graph.attributes())  
        
        def __delitem__(self,key):
            s = 'do not use'
            
    class PropertiesDict(collections.MutableMapping):
        """A dictionary interface to underlying Graph attributes."""
    
        def __init__(self, *args, **kwargs):
            self._attr=kwargs.get('_attr')
            self._type=kwargs.get('_type')
            self._graph = kwargs.get('_graph')
        
        def __repr__(self):
            if self._type == 'vs':
                return str(self._graph.vs[self._attr])
            elif self._type == 'es':
                return str(self._graph.es[self._attr])
            elif self._type == 'g':
                return str(self._graph[self._attr])
    
        def __getitem__(self, key):
            if self._type == 'vs':
                return self._graph.vs[self._graph._get_id(key)][self._attr]
            elif self._type == 'es':
                return self._graph.es[self._graph._get_id(key)][self._attr]
            elif self._type == 'g':
                return self._graph[key]
                
        def __setitem__(self, key, value):
            if self._type == 'vs':
                self._graph.vs[self._graph._get_id(key)][self._attr] = value
            elif self._type == 'es':
                self._graph.es[self._graph._get_id(key)][self._attr] = value
    
        def __iter__(self):
            if self._type == 'vs':
                return iter(self._graph.vs[self._attr])
            elif self._type == 'es':
                return iter(self._graph.es[self._attr])
            elif self._type == 'g':
                return iter(self._graph[self._attr])
            
        def __len__(self):
            if self._type == 'vs':
                return len(self._graph.vs[self._attr])
            elif self._type == 'es':
                return len(self._graph.es[self._attr])
            elif self._type == 'g':
                return len(self._graph[self._attr])   
            
        def __delitem__(self,key):
            s = 'do not use'
         
    def __init__(self, *args, **kwds):
        super(Graph,self).__init__(*args,**kwds)
        self.edge_properties = self.PropertiesDictWrapper(_graph=self,_type='es')
        self.vertex_properties = self.PropertiesDictWrapper(_graph=self,_type='vs')
        self.graph_properties = self.PropertiesDictWrapper(_graph=self,_type='g')
        
        #for filter functionality
        self._unfiltered_graph = None
        self._filtered = False
                    
    '''Methods related to filtering.'''
    def set_filters(self,vsel,esel,inverted_vertices=False,inverted_edges=False):
        self.set_vertex_filter(vsel,inverted_vertices)
        self.set_edge_filter(esel,inverted_edges)
    
    def set_vertex_filter(self,sel,inverted=False):
        if sel:
            if self._filtered == False:
                self._unfiltered_graph = deepcopy(self)
                self._filtered = True
            
            if type(sel)==VertexSeq or all(type(item) is int for item in sel):
                sel = sel.indices if type(sel)==VertexSeq else sel                
                complement = list(set([i for i in range(0,self.vcount())]) - set(sel))
                self = self.delete_vertices(complement)
            elif len(sel) == self.vcount():
                self = self.delete_vertices([i for i, b in enumerate(sel) if inverted == bool(b)])
            
    def set_edge_filter(self,sel,inverted=False):
        if sel:
            if self._filtered == False:
                self._unfiltered_graph = deepcopy(self)
                self._filtered = True
            
            if type(sel)==EdgeSeq or all(type(item) is int for item in sel):
                sel = sel.indices if type(sel)==EdgeSeq else sel                
                complement = list(set([i for i in range(0,self.ecount())]) - set(sel))
                self = self.delete_edges(complement)
            elif len(sel) == self.ecount():
                self = self.delete_edges([i for i, b in enumerate(sel) if inverted == bool(b)])
    
    def purge_vertices(self):
        if self._filtered:
            self._filtered = False
            self._unfiltered_graph = None
            
    def purge_edges(self):
        self.purge_vertices()   
    
    def clear_filters(self):
        self = self._unfiltered_graph
        self._filtered = False
        return self._unfiltered_graph
        
    '''Methods for setting up/accessing graph attributes.'''
    def set_directed(self,b):
        if b == True:
            self = self.as_directed()
        elif b == False:
            self = self.as_undirected()
    
    def new_vertex_property(self, t):
        return self.PropertiesDict(_graph=self,_type='vs')
    
    def new_vp(self,t):
        return self.new_vertex_property(t)
        
    def new_edge_property(self,t):
        return self.PropertiesDict(_graph=self,_type='es')
    
    def new_ep(self,t):
        return self.new_edge_property(t)
    
    def new_graph_property(self, t):
        return None
        
    def new_gp(self,t):
        return self.new_graph_property(t)
                
    def out_degree(self):
        pass
        #return self.outdegree()
        
    def _get_id(self,o):
        if type(o) == int:
            return o
        elif hasattr(o,'index'):
            return o.index
        else:
            raise ValueError("Object has no index attribute or is not an int.")
    
    def reindex_edges():
        pass
        
    '''Methods for adding/accessing vertices or edges.'''
    def add_edge(self,v,w):
        vid = self._get_id(v)
        wid = self._get_id(w)       
        
        super(Graph,self).add_edge(vid,wid)     
        e = self.es[self.ecount()-1]
      
        
        for prop in self.edge_properties:
            self.edge_properties[prop][e] = None
            
        return e
    
    def add_vertex(self,n=1):
        super(Graph,self).add_vertices(n)
        
        for prop in self.vertex_properties:
            for v in self.vs[-n:]:
                self.vertex_properties[prop][v] = None
        
        if n == 1:
            return self.vs[self.vcount()-1]
        else:
            return iter(self.vs[-n:])
        
    def num_edges(self):
        return self.ecount()
    
    def num_vertices(self):
        return self.vcount()
    
    def edge(self,v,w,**kwds):
        try:
            return self.es.find(_source=self._get_id(v),_target=self._get_id(w))
        except ValueError as e:
            if kwds.get('add_missing'):
                return self.add_edge(v,w)
            return None
        
    def vertex(self,i,**kwds):
        if i < self.vcount():
            return self.vs[i]
        else:
            if kwds.get('add_missing'):
                self.add_vertex( i + 1 - self.vcount() )
                return self.vs[self.vcount()-1]
            raise ValueError("Invalid vertex index. Call with 'add_missing=True' to add.")
    
    def vertices(self):
        return iter(self.vs)
    
    def edges(self):
        return iter(self.es)
    
    def remove_vertex(self,v):
        self.delete_vertices(self._get_id(v))
        
    def remove_edge(self,e):
        self.delete_edges(self._get_id(e))
        
    '''Methods for analysis.'''
    def __local_clustering__(self,graph,weights=None):
        
        return self.transitivity_local_undirected(vertices=graph.vs,weights=weights)
    
class Edge(Edge):
    
    def source(self):
        return self.graph.vs[self.source]
    
    def target(self):
        return self.graph.vs[self.target]
    
'''Functions for analysis.''' #TODO