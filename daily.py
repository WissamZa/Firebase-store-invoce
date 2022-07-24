from dataclasses import dataclass, field


@dataclass
class dailys:
    date: str
    inCash: float
    inCrdit: float
    outgoing: float = 0.0
    inTotal: float = field(init=False, default=0)
    totalNet: float= field(init=False,default=0)

    def __post_init__(self):
        self.inTotal = self.inCash + self.inCrdit
        self.totalNet = self.inTotal - self.outgoing


if __name__ == "__main__":
    pass
