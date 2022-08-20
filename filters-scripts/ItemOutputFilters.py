class OutputFilter_base:
    def __init__(self):
        pass

    def CastIntoList(self,
                     data):
        if type(data) == str:
            data = [data]
        return data

    def Parse(self,
                  data):
        raise NotImplementedError

class RemoveFirst_A(OutputFilter_base):
    #  remove the first A:
    def __init__(self):
        super().__init__()

    def Parse(self,
                  data):
        data = self.CastIntoList(data)
        # since it works on string, I convert promptdesignerdataset to string and back to list again
        data = '\n'.join(data)
        data = data.replace('A:', '', 1).strip()
        return self.CastIntoList(data)

class ClearListItems(OutputFilter_base):
    #  remove the " -' ' " from each item
    def __init__(self):
        super().__init__()
    def Parse(self,
                  data):
        def parseitem(item):
            item = item.replace('-', '', 1)
            item = item.replace("'", '', 1)
            item = item.replace("'", '', 1)
            item = item.strip()
            return item

        if type(data) == str:
            return parseitem(data)
        return [parseitem(item) for item in data]

class MakeUppercase(OutputFilter_base):
    # makes all uppercase
    def __init__(self):
        super().__init__()

    def Parse(self,
                  data):
        if type(data) == str:
            return data.upper()
        else:
            res = list()
            for item in data:
                res.extend(item.upper())
            return res

class RemoveEmptyItem(OutputFilter_base):
    #  remove empty items
    def __init__(self):
        super().__init__()

    def Parse(self,
              data):
        if type(data) == str:
            return data
        else:
            res = list()
            for item in data:
                if item.strip():
                    res.append(item)
            return res


class ExtractItemsList(OutputFilter_base):
    #  return a list of items. essentially perform split(\n)

    def __init__(self):
        super().__init__()

    def Parse(self,
                  data):
        if type(data) == str:
            return data.split('\n')
        else:
            items = list()
            for dat in data:
                for d in dat.split('\n'):
                    items.append(d.strip())
            return items
