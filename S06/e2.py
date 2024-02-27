from seq import Seq

seq_list = [Seq("ACT"), Seq("GATA"), Seq("CAGATA")]
for s in seq_list:
    print(f"Sequence {seq_list.index(s)}: (Length: {s.len()}) {s}")




