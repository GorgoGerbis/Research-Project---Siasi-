from src.NodeObj import NodeObj


class LinkObj(NodeObj):  # Most likely need to make this a subclass of NodeObj

    def __init__(self, linkID, linkSrc, linkDest, linkBW, linkED, linkEC, linkWeight):
        self.linkID = linkID
        self.linkSrc = linkSrc
        self.linkDest = linkDest
        self.linkBW = linkBW
        self.linkED = linkED
        self.linkEC = linkEC
        self.linkWeight = linkWeight

        NodeObj.StaticLinkList.append(self)

    def showLinkSourceID(self):
        return self.linkSrc

    def compareBW(self, bw):
        if self.linkBW >= bw:
            return True
        else:
            return False

    def map_request(self, bw):
        self.linkBW = int(self.linkBW) - bw

    def check_enough_resources(self, req_bw):
        if self.compareBW(req_bw):
            self.map_request(req_bw)
            print("LINK HAS BEEN TRAVERSED")
            return 0
        else:
            print("NOT ENOUGH RESOURCES FOR TRAVERSAL")
            return 1

    # This method has to be static so that it can be accessed everywhere basically just a helper function
    @staticmethod
    def returnLink(link_id):
        for link in NodeObj.StaticLinkList:
            if link.linkID == link_id:
                return link

    def __str__(self):
        string = "LinkID {} Source {} Dest {} BandWidth {} Delay {} Cost {} Weight {}".format(self.linkID, self.linkSrc, self.linkDest, self.linkBW, self.linkED, self.linkEC, self.linkWeight)
        return string