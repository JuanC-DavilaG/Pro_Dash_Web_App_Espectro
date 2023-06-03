# Clases para extraer información del plotly.graph_object Figure()
class TraceInfoData:
    def __init__(self, figure):
        self.fig = figure
        self.traces = self.__traces()
        self.number = self.__len__()
        self.names = self.__trace_names()

    def __getitem__(self, index):
        return self.traces[index]

    def __len__(self):
        return len(self.traces)

    def __traces(self):
        return list(self.fig.data)

    def __trace_names(self):
        return [trace.name for trace in self.traces]

class TraceInfoLayout:
    def __init__(self, figure):
        self.fig = figure
        self.traces = self.__layout()
        self.number = self.__len__()
        self.names = self.__layout_names()
        self.tamView = self.__layout_view()

    def __getitem__(self, index):
        return self.traces[index]

    def __len__(self):
        return len(self.traces)

    def __layout(self):
        return list(self.fig.layout.shapes)
    
    def __layout_names(self):
        return [trace.name for trace in self.traces]
    
    def __layout_view(self):
        return self.fig.layout.xaxis.range
