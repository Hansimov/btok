import json

from pathlib import Path
from typing import Union

PARENT_DIR = Path(__file__).parent


class ChineseSimplifier:
    """Convert Chinese traditional to simplified.
    Thanks to zhconv for the idea and data:
    https://github.com/gumblex/zhconv/blob/master/zhconv/zhcdict.json"""

    def __init__(self):
        self.dict_path = PARENT_DIR / "zh.json"
        self.load_dict()

    def load_dict(self):
        """Load traditional-simplified dictionary."""
        with open(self.dict_path, "r", encoding="utf-8") as rf:
            self.zh_dict = json.load(rf)
        self.zh2hans_dict = self.zh_dict.get("zh2hans", {})
        self.zh2hans_dict = self.remove_same_key_val(self.zh2hans_dict)

    def remove_same_key_val(self, data_dict: dict):
        """Remove items with same key and value."""
        return {k: v for k, v in data_dict.items() if k != v}

    def dump_dict(self, out_path: Union[str, Path]):
        """Dump the traditional-simplified dictionary to a json file."""
        out_path = Path(out_path)
        with open(out_path, "w", encoding="utf-8") as wf:
            json.dump(self.zh2hans_dict, wf, ensure_ascii=False, indent=4)

    def contain_traditional(self, sentence: str) -> bool:
        """Check if sentence contains any traditional char.
        This is to avoid unnecessary list operations."""
        for ch in sentence:
            if ch in self.zh2hans_dict:
                return True
        return False

    def simplify(
        self, sentence: str, return_vocab: bool = False
    ) -> Union[str, tuple[str, dict[str]]]:
        """Convert Chinese traditional to simplified."""
        if not self.contain_traditional(sentence):
            if return_vocab:
                return sentence, {}
            else:
                return sentence
        res = []
        vocab = {}
        for ch in sentence:
            if ch in self.zh2hans_dict:
                ch_s = self.zh2hans_dict[ch]
                res.append(ch_s)
                if return_vocab:
                    vocab[ch] = ch_s
            else:
                res.append(ch)
        if return_vocab:
            vocab_r = {v: k for k, v in vocab.items() if k != v}
            return "".join(res), vocab_r
        else:
            return "".join(res)

    def convert_back(self, sentence: str, vocab: dict) -> str:
        """Convert simplified chars back to traditional by vocab."""
        is_contain_vocab = False
        for ch in sentence:
            if ch in vocab:
                is_contain_vocab = True
                break
        if not is_contain_vocab:
            return sentence
        res = []
        for ch in sentence:
            if ch in vocab:
                res.append(vocab[ch])
            else:
                res.append(ch)
        return "".join(res)


def test_dump_dict():
    """Dump the traditional-simplified dictionary to a json file."""
    simplifier = ChineseSimplifier()
    output_path = PARENT_DIR / "zh2hans_reduced.json"
    simplifier.dump_dict(output_path)


if __name__ == "__main__":
    test_dump_dict()

    # python -m src.btok.simplify
